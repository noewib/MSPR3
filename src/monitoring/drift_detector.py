import json
import os
import numpy as np
import pandas as pd

try:
    from scipy.stats import ks_2samp

    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

from src.data.data_pipeline import DataPipeline


class DriftDetector:
    def __init__(self, threshold_pvalue=0.05):
        self.threshold_pvalue = threshold_pvalue

    def calculate_drift(
        self, reference_df: pd.DataFrame, current_df: pd.DataFrame, features: list
    ) -> dict:
        """
        Compare reference training data with recent RTE data.
        """
        results = {}

        for feature in features:
            if feature not in reference_df.columns or feature not in current_df.columns:
                continue

            ref = reference_df[feature].dropna().values
            cur = current_df[feature].dropna().values

            if len(ref) == 0 or len(cur) == 0:
                results[feature] = {
                    "drift_detected": False,
                    "method": "insufficient_data",
                }
                continue

            if HAS_SCIPY:
                stat, p_val = ks_2samp(ref, cur)
                results[feature] = {
                    "drift_detected": bool(p_val < self.threshold_pvalue),
                    "method": "Kolmogorov-Smirnov",
                    "statistic": float(stat),
                    "p_value": float(p_val),
                }
            else:
                ref_mean = float(np.mean(ref))
                cur_mean = float(np.mean(cur))
                ref_std = float(np.std(ref)) or 1.0
                drift = abs(cur_mean - ref_mean) > 2 * ref_std

                results[feature] = {
                    "drift_detected": bool(drift),
                    "method": "mean_std_fallback",
                    "reference_mean": ref_mean,
                    "current_mean": cur_mean,
                }

        return results


def main():
    print("--- Running RTE Eco2mix Drift Detection ---")

    pipeline = DataPipeline()

    print("Loading real RTE Eco2mix files...")
    raw = pipeline.load_rte_folder("data/raw")

    print("Aggregating RTE data to daily level...")
    daily = pipeline.aggregate_to_daily(raw)

    print("Creating features...")
    prepared = pipeline.feature_engineering(daily, is_training=True)

    split_idx = int(len(prepared) * 0.8)
    reference_df = prepared.iloc[:split_idx].copy()
    current_df = prepared.iloc[split_idx:].copy()

    features = [
        "target_consumption_mw",
        "forecast_j_1",
        "forecast_j",
        "nuclear",
        "wind",
        "solar",
        "gas",
        "hydraulic",
        "co2_rate",
    ]

    detector = DriftDetector(threshold_pvalue=0.05)
    results = detector.calculate_drift(reference_df, current_df, features)

    os.makedirs("models", exist_ok=True)

    report = {
        "data_source": pipeline.data_source_,
        "reference_period": [
            str(reference_df["date"].min()),
            str(reference_df["date"].max()),
        ],
        "current_period": [
            str(current_df["date"].min()),
            str(current_df["date"].max()),
        ],
        "features_checked": features,
        "method": "Kolmogorov-Smirnov if scipy is available, otherwise mean/std fallback",
        "results": results,
    }

    with open("models/drift_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    print(json.dumps(report, indent=2, ensure_ascii=False))
    print("Drift report saved to models/drift_report.json")


if __name__ == "__main__":
    main()
