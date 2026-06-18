import random
from datetime import datetime, timedelta

from locust import HttpUser, task, between


class ElectricityPredictorUser(HttpUser):
    # Simulate users/systems calling the API every 1 to 3 seconds
    wait_time = between(1, 3)

    def on_start(self):
        self.base_date = datetime(2025, 1, 15)

    @task(8)
    def post_prediction_request(self):
        """Simulate sending a valid prediction request to /predict."""

        random_days = random.randint(-30, 30)
        target_date = self.base_date + timedelta(days=random_days)

        # Simulated but schema-valid daily RTE-like payload
        forecast_j = random.uniform(45000, 70000)
        forecast_j_1 = forecast_j + random.normalvariate(0, 800)

        payload = {
            "date": target_date.strftime("%Y-%m-%d"),
            "forecast_j_1": round(forecast_j_1, 1),
            "forecast_j": round(forecast_j, 1),
            "lag_1d": round(forecast_j + random.normalvariate(0, 1200), 1),
            "lag_7d": round(forecast_j + random.normalvariate(0, 1500), 1),
            "lag_14d": round(forecast_j + random.normalvariate(0, 1800), 1),
            "rolling_mean_7d": round(forecast_j + random.normalvariate(0, 1000), 1),
            "rolling_mean_30d": round(forecast_j + random.normalvariate(0, 1200), 1),
            "fioul": round(random.uniform(50, 500), 1),
            "coal": round(random.uniform(20, 400), 1),
            "gas": round(random.uniform(1500, 7000), 1),
            "nuclear": round(random.uniform(30000, 50000), 1),
            "wind": round(random.uniform(1000, 12000), 1),
            "solar": round(random.uniform(0, 8000), 1),
            "hydraulic": round(random.uniform(3000, 12000), 1),
            "pumping": round(random.uniform(-1500, 500), 1),
            "bioenergy": round(random.uniform(500, 1200), 1),
            "physical_exchanges": round(random.uniform(-8000, 8000), 1),
            "co2_rate": round(random.uniform(20, 90), 1),
        }

        with self.client.post("/predict", json=payload, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(
                    f"Prediction failed with status {response.status_code}: {response.text}"
                )

    @task(1)
    def check_health(self):
        """Simulate health probes checking the API status."""
        self.client.get("/health")

    @task(1)
    def fetch_metrics(self):
        """Simulate Prometheus scraping the metrics endpoint."""
        self.client.get("/metrics")
