import unittest
import pandas as pd
import numpy as np
from src.data.data_pipeline import DataPipeline


class TestDataPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = DataPipeline()

    def test_aggregate_and_features(self):
        dates = pd.date_range("2024-01-01", periods=60 * 48, freq="30min")
        raw = pd.DataFrame({
            "datetime": dates,
            "consumption": 50000 + np.sin(np.arange(len(dates)) / 10) * 1000,
            "forecast_j_1": 50000,
            "forecast_j": 50100,
            "nuclear": 40000,
            "wind": 5000,
            "solar": 1000,
            "gas": 3000,
            "hydraulic": 8000,
            "co2_rate": 30,
        })

        daily = self.pipeline.aggregate_to_daily(raw)
        feats = self.pipeline.feature_engineering(daily, is_training=True)

        self.assertIn("target_consumption_mw", feats.columns)
        self.assertIn("lag_7d", feats.columns)
        self.assertFalse(feats[self.pipeline.feature_cols].isnull().any().any())

    def test_fit_transform(self):
        dates = pd.date_range("2024-01-01", periods=90 * 48, freq="30min")
        raw = pd.DataFrame({
            "datetime": dates,
            "consumption": 50000 + np.random.normal(0, 1000, len(dates)),
            "forecast_j_1": 50000,
            "forecast_j": 50100,
        })

        daily = self.pipeline.aggregate_to_daily(raw)
        feats = self.pipeline.feature_engineering(daily, is_training=True)

        self.assertGreater(len(feats), 0)

        X, y = self.pipeline.fit_transform_prepared(feats)

        self.assertEqual(len(X), len(y))
        self.assertEqual(X.shape[1], len(self.pipeline.feature_cols))


if __name__ == "__main__":
    unittest.main()