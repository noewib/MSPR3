import random
from datetime import datetime, timedelta
from locust import HttpUser, task, between

class ElectricityPredictorUser(HttpUser):
    # Wait between 1 and 3 seconds between tasks to simulate human dispatchers/systems
    wait_time = between(1, 3)

    def on_start(self):
        """Called when a virtual user starts running."""
        # Generate some base data for this user session
        self.base_date = datetime.now()

    @task(8)
    def post_prediction_request(self):
        """Simulate sending a prediction request to /predict."""
        # Create a random timestamp in the near future/past
        random_hours = random.randint(-48, 48)
        target_time = self.base_date + timedelta(hours=random_hours)
        
        # Simulate realistic features
        # Temperature: 5°C to 28°C
        temp = round(random.uniform(5.0, 28.0), 1)
        
        # Base consumption roughly thermosensitive: ~45000 MW in summer, ~75000 MW in winter
        approx_base = 55000.0 + max(0.0, 15.0 - temp) * 1800.0
        
        payload = {
            "datetime": target_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "temperature": temp,
            "lag_24h": round(approx_base + random.normalvariate(0, 1000), 1),
            "lag_48h": round(approx_base + random.normalvariate(0, 1000), 1),
            "lag_7d": round(approx_base + random.normalvariate(0, 1000), 1),
            "temp_roll_mean_3h": round(temp + random.uniform(-0.5, 0.5), 1),
            "temp_roll_mean_6h": round(temp + random.uniform(-1.0, 1.0), 1)
        }
        
        headers = {"Content-Type": "application/json"}
        
        # POST request
        with self.client.post("/predict", json=payload, headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Prediction failed with status {response.status_code}: {response.text}")

    @task(1)
    def check_health(self):
        """Simulate health probes checking the API health status."""
        self.client.get("/health")

    @task(1)
    def fetch_metrics(self):
        """Simulate Prometheus scraping the metrics endpoint."""
        self.client.get("/metrics")
