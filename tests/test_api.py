import unittest
from fastapi.testclient import TestClient
from src.api.app import app, load_model_and_pipeline

class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Trigger default model generation on startup
        load_model_and_pipeline()
        cls.client = TestClient(app)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_metrics_endpoint(self):
        response = self.client.get("/metrics")
        self.assertEqual(response.status_code, 200)
        self.assertIn("http_requests_total", response.text)

    def test_predict_endpoint_success(self):
        payload = {
            "datetime": "2026-05-28T19:00:00",
            "temperature": 12.5,
            "lag_24h": 58000.0,
            "lag_48h": 57500.0,
            "lag_7d": 59000.0,
            "temp_roll_mean_3h": 12.0,
            "temp_roll_mean_6h": 11.5
        }
        response = self.client.post("/predict", json=payload)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("prediction_mw", data)
        self.assertIn("latency_sec", data)
        self.assertTrue(data["prediction_mw"] > 0)

    def test_predict_endpoint_missing_optional_fields(self):
        # Verify that optional fields are auto-filled and prediction works
        payload = {
            "datetime": "2026-05-28T19:00:00",
            "temperature": 15.0
        }
        response = self.client.post("/predict", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")

    def test_predict_endpoint_invalid_date(self):
        payload = {
            "datetime": "invalid-date-format",
            "temperature": 15.0
        }
        response = self.client.post("/predict", json=payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid datetime format", response.json()["detail"])

if __name__ == '__main__':
    unittest.main()
