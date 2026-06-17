import unittest
import pandas as pd
import numpy as np
from src.data.data_pipeline import DataPipeline


class TestDataPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = DataPipeline()

    def test_generate_historical_data(self):
        # Generate 5 days of data
        df = self.pipeline.generate_historical_data(days=5)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertIn("datetime", df.columns)
        self.assertIn("temperature", df.columns)
        self.assertIn("consommation", df.columns)

        # 5 days * 48 records per day (half-hourly) = 240 + 1 (endpoint)
        self.assertGreaterEqual(len(df), 240)

    def test_feature_engineering(self):
        df_raw = self.pipeline.generate_historical_data(days=10)

        # Test training feature engineering (drops nan values from shift)
        df_feats = self.pipeline.feature_engineering(df_raw, is_training=True)

        # Check required columns
        for col in self.pipeline.feature_cols:
            self.assertIn(col, df_feats.columns)

        # Check cyclical values are within [-1, 1]
        self.assertTrue(
            (df_feats["hour_sin"] >= -1.0).all() and (df_feats["hour_sin"] <= 1.0).all()
        )
        self.assertTrue(
            (df_feats["month_cos"] >= -1.0).all()
            and (df_feats["month_cos"] <= 1.0).all()
        )

        # Lags check (should have no null values since drops were done)
        self.assertFalse(df_feats["lag_24h"].isnull().any())
        self.assertFalse(df_feats["lag_7d"].isnull().any())

    def test_fit_transform_scaling(self):
        df_raw = self.pipeline.generate_historical_data(days=15)
        X_scaled, y = self.pipeline.fit_transform(df_raw)

        self.assertEqual(len(X_scaled), len(y))
        self.assertEqual(X_scaled.shape[1], len(self.pipeline.feature_cols))

        # Scaled values mean should be roughly 0 and standard deviation roughly 1
        # (StandardScaler behavior)
        self.assertAlmostEqual(np.mean(X_scaled[:, 0]), 0.0, places=1)
        self.assertAlmostEqual(np.std(X_scaled[:, 0]), 1.0, places=1)


if __name__ == "__main__":
    unittest.main()
