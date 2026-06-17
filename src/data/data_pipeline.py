import datetime
import numpy as np
import pandas as pd
import requests
import os

try:
    import holidays

    HAS_HOLIDAYS = True
except ImportError:
    HAS_HOLIDAYS = False


class DataPipeline:
    def __init__(self):
        self.scaler = None
        self.feature_cols = [
            "temperature",
            "hour_sin",
            "hour_cos",
            "month_sin",
            "month_cos",
            "day_of_week",
            "is_weekend",
            "is_holiday",
            "lag_24h",
            "lag_48h",
            "lag_7d",
            "temp_roll_mean_3h",
            "temp_roll_mean_6h",
        ]
        self.target_col = "consommation"

    def fetch_realtime_data(self, limit=100) -> pd.DataFrame:
        """
        Fetch recent power grid data from ODRE (Open Data Réseaux Électriques) API.
        Falls back to generating realistic mock data if the API is down or unavailable.
        """
        url = f"https://odre.opendatasoft.com/api/v2/catalog/datasets/eco2mix-national-tr/records?limit={limit}&order_by=date_heure%20desc"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                records = response.json().get("records", [])
                if records:
                    data_list = []
                    for r in records:
                        fields = r.get("record", {}).get("fields", {})
                        # Translate fields to standard column names
                        data_list.append(
                            {
                                "datetime": pd.to_datetime(fields.get("date_heure")),
                                "consommation": fields.get("consommation"),
                                # If temperature is not in ODRE direct records, we simulate it
                                "temperature": fields.get(
                                    "temperature",
                                    self._generate_simulated_temp(
                                        pd.to_datetime(fields.get("date_heure"))
                                    ),
                                ),
                            }
                        )
                    df = pd.DataFrame(data_list)
                    df = (
                        df.dropna(subset=["consommation"])
                        .sort_values("datetime")
                        .reset_index(drop=True)
                    )
                    if not df.empty:
                        return df
        except Exception as e:
            print(
                f"Warning: ODRE API call failed ({e}). Falling back to simulated data."
            )

        # Fallback to simulated data for the last few days
        now = datetime.datetime.now()
        start = now - datetime.timedelta(days=3)
        return self.generate_historical_data(start_date=start, end_date=now)

    def _generate_simulated_temp(self, dt: datetime.datetime) -> float:
        """Helper to generate temperature based on date/hour for France."""
        day_of_year = dt.timetuple().tm_yday
        hour = dt.hour + dt.minute / 60.0

        # Annual cycle: min in Jan (day 15), max in July (day 200)
        # Average temp around 12.5°C, amplitude 9°C
        yearly_temp = 12.5 - 9.0 * np.cos(2 * np.pi * (day_of_year - 15) / 365.0)

        # Daily cycle: peak around 15h, amplitude 4°C
        daily_temp = 4.0 * np.cos(2 * np.pi * (hour - 15) / 24.0)

        return float(np.round(yearly_temp + daily_temp, 2))

    def generate_historical_data(
        self, start_date=None, end_date=None, days=365
    ) -> pd.DataFrame:
        """
        Generate high-fidelity synthetic national consumption & temperature data.
        Models seasonal variation, daily peaks, weekend drops, holidays, and thermosensitivity.
        """
        if end_date is None:
            end_date = datetime.datetime.now()
        if start_date is None:
            start_date = end_date - datetime.timedelta(days=days)

        date_range = pd.date_range(start=start_date, end=end_date, freq="30min")

        df = pd.DataFrame({"datetime": date_range})

        # Generate weather
        df["temperature"] = df["datetime"].apply(self._generate_simulated_temp)
        # Add small random walk noise to temperature
        np.random.seed(42)
        temp_noise = np.random.normal(0, 0.5, len(df)).cumsum()
        # Scale noise to keep it bounded
        temp_noise = 2.0 * np.sin(np.arange(len(df)) / 100) + np.random.normal(
            0, 0.3, len(df)
        )
        df["temperature"] += temp_noise
        df["temperature"] = df["temperature"].round(2)

        # Generate consumption (thermosensitive model)
        # Base load
        base = 50000.0  # MW

        # Seasonal cycle
        # Heating in France triggers below ~15°C: roughly +2000 MW per degree below 15
        thermo_threshold = 15.0
        thermosensitivity = df["temperature"].apply(
            lambda t: max(0.0, thermo_threshold - t) * 1800.0
        )

        # Daily cycle (peak around 8h-13h and 18h-21h)
        hour = df["datetime"].dt.hour + df["datetime"].dt.minute / 60.0
        daily_factor = 5000.0 * np.sin(2 * np.pi * (hour - 6) / 24.0) + 3000.0 * np.sin(
            4 * np.pi * (hour - 15) / 24.0
        )

        # Weekly factor (weekend drop of ~15%)
        day_of_week = df["datetime"].dt.dayofweek
        weekly_factor = np.where(day_of_week >= 5, -6000.0, 0.0)

        # Holiday factor (similar to Sunday)
        fr_holidays = holidays.France() if HAS_HOLIDAYS else {}
        is_holiday = df["datetime"].dt.date.apply(lambda d: d in fr_holidays)
        holiday_factor = np.where(is_holiday, -6000.0, 0.0)

        # Noise
        noise = np.random.normal(0, 800.0, len(df))

        df["consommation"] = (
            base
            + thermosensitivity
            + daily_factor
            + weekly_factor
            + holiday_factor
            + noise
        )
        df["consommation"] = df["consommation"].round(0)

        return df

    def feature_engineering(
        self, df: pd.DataFrame, is_training: bool = True
    ) -> pd.DataFrame:
        """
        Enrich data with cyclical, calendary, lag, and rolling features.
        """
        df = df.copy()
        df = df.sort_values("datetime").reset_index(drop=True)

        # Calendary components
        df["hour"] = df["datetime"].dt.hour + df["datetime"].dt.minute / 60.0
        df["month"] = df["datetime"].dt.month
        df["day_of_week"] = df["datetime"].dt.dayofweek
        df["is_weekend"] = (df["day_of_week"] >= 5).astype(int)

        # French Holidays
        if HAS_HOLIDAYS:
            fr_holidays = holidays.France()
            df["is_holiday"] = (
                df["datetime"].dt.date.apply(lambda d: d in fr_holidays).astype(int)
            )
        else:
            # Fallback simple holiday check (approximate major ones)
            # Jan 1, May 1, May 8, July 14, Aug 15, Nov 1, Nov 11, Dec 25
            major_holidays = [
                (1, 1),
                (5, 1),
                (5, 8),
                (7, 14),
                (8, 15),
                (11, 1),
                (11, 11),
                (12, 25),
            ]
            df["is_holiday"] = (
                df["datetime"]
                .apply(lambda row: 1 if (row.month, row.day) in major_holidays else 0)
                .astype(int)
            )

        # Cyclical encoding
        df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24.0)
        df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24.0)
        df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12.0)
        df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12.0)

        # Lag features (half-hourly steps: 24h = 48 steps, 48h = 96 steps, 7d = 336 steps)
        # Shift target variable
        df["lag_24h"] = df[self.target_col].shift(48)
        df["lag_48h"] = df[self.target_col].shift(96)
        df["lag_7d"] = df[self.target_col].shift(336)

        # Rolling metrics (temperature inertia, half-hourly steps: 3h = 6 steps, 6h = 12 steps)
        df["temp_roll_mean_3h"] = (
            df["temperature"].rolling(window=6, min_periods=1).mean()
        )
        df["temp_roll_mean_6h"] = (
            df["temperature"].rolling(window=12, min_periods=1).mean()
        )

        # Handle NaN values introduced by shift (e.g. fill with backfill/median or drop)
        if is_training:
            # During training, drop rows that don't have lag data
            df = df.dropna(subset=["lag_24h", "lag_48h", "lag_7d"])
        else:
            # During inference, if lags are missing, we can forward fill or impute
            # For robustness:
            df["lag_24h"] = df["lag_24h"].bfill().fillna(df[self.target_col].mean())
            df["lag_48h"] = df["lag_48h"].bfill().fillna(df[self.target_col].mean())
            df["lag_7d"] = df["lag_7d"].bfill().fillna(df[self.target_col].mean())

        return df.reset_index(drop=True)

    def fit_transform(self, df: pd.DataFrame) -> tuple[np.ndarray, np.ndarray]:
        """
        Fit scaler and scale features for model training.
        """
        from sklearn.preprocessing import StandardScaler

        df_feats = self.feature_engineering(df, is_training=True)
        X = df_feats[self.feature_cols].values
        y = df_feats[self.target_col].values

        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)

        return X_scaled, y

    def transform(self, df: pd.DataFrame) -> np.ndarray:
        """
        Scale features for model inference.
        """
        if self.scaler is None:
            raise ValueError("Scaler is not fitted yet. Call fit_transform first.")

        df_feats = self.feature_engineering(df, is_training=False)
        X = df_feats[self.feature_cols].values

        return self.scaler.transform(X)
