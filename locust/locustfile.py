"""
Locust Load Test — EDF/RTE Electricity Consumption Predictor API

Usage:
    locust -f locust/locustfile.py --host http://127.0.0.1:8000
    locust -f locust/locustfile.py --host http://127.0.0.1:8000 --headless -u 1000 -r 50 -t 120s
"""

import logging
import random
import time
from datetime import datetime, timedelta

from locust import HttpUser, LoadTestShape, between, events, task

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# Event handlers
# ─────────────────────────────────────────────

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Called when a load test is started."""
    logger.info("=" * 60)
    logger.info("  ⚡ EDF/RTE Predictor — Test de charge démarré")
    logger.info(f"  🎯 Host: {environment.host}")
    logger.info(f"  ⏰ Heure de début: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Called when a load test is stopped."""
    stats = environment.runner.stats
    logger.info("=" * 60)
    logger.info("  🏁 Test de charge terminé")
    logger.info(f"  ⏰ Heure de fin: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"  📊 Total requêtes: {stats.total.num_requests}")
    logger.info(f"  ❌ Total échecs: {stats.total.num_failures}")
    if stats.total.num_requests > 0:
        fail_rate = (stats.total.num_failures / stats.total.num_requests) * 100
        logger.info(f"  📉 Taux d'échec: {fail_rate:.2f}%")
    logger.info(f"  ⏱️ Temps de réponse moyen: {stats.total.avg_response_time:.0f}ms")
    logger.info(f"  ⏱️ P95: {stats.total.get_response_time_percentile(0.95):.0f}ms")
    logger.info("=" * 60)


# ─────────────────────────────────────────────
# Payload generators
# ─────────────────────────────────────────────

def generate_valid_payload():
    """Generate a realistic /predict payload matching PredictRequest schema."""
    base = datetime(2024, 1, 1)
    random_days = random.randint(0, 500)
    target_date = base + timedelta(days=random_days)

    # Seasonal consumption pattern
    month = target_date.month
    if month in (12, 1, 2):
        base_conso = random.uniform(60000, 80000)
    elif month in (6, 7, 8):
        base_conso = random.uniform(38000, 52000)
    else:
        base_conso = random.uniform(48000, 65000)

    noise = lambda: random.normalvariate(0, 2000)

    return {
        "date": target_date.strftime("%Y-%m-%d"),
        "forecast_j_1": round(base_conso + noise(), 1),
        "forecast_j": round(base_conso + noise(), 1),
        "lag_1d": round(base_conso + noise(), 1),
        "lag_7d": round(base_conso + noise(), 1),
        "lag_14d": round(base_conso + noise(), 1),
        "rolling_mean_7d": round(base_conso + random.uniform(-1000, 1000), 1),
        "rolling_mean_30d": round(base_conso + random.uniform(-500, 500), 1),
        "fioul": round(random.uniform(0, 500), 1),
        "coal": round(random.uniform(0, 300), 1),
        "gas": round(random.uniform(2000, 8000), 1),
        "nuclear": round(random.uniform(25000, 42000), 1),
        "wind": round(random.uniform(1000, 15000), 1),
        "solar": round(random.uniform(0, 12000), 1),
        "hydraulic": round(random.uniform(4000, 14000), 1),
        "pumping": round(random.uniform(-3000, 0), 1),
        "bioenergy": round(random.uniform(500, 1200), 1),
        "physical_exchanges": round(random.uniform(-8000, 5000), 1),
        "co2_rate": round(random.uniform(20, 90), 1),
    }


def generate_malformed_payload():
    """Generate a malformed payload for failure testing."""
    malformed_type = random.choice([
        "missing_required",
        "wrong_types",
        "empty_body",
        "extra_garbage",
        "invalid_date",
    ])

    if malformed_type == "missing_required":
        # Only include some optional fields, no date
        return {"nuclear": 35000.0, "wind": 8000.0}
    elif malformed_type == "wrong_types":
        return {
            "date": 12345,
            "forecast_j_1": "not_a_number",
            "nuclear": None,
            "gas": [1, 2, 3],
        }
    elif malformed_type == "empty_body":
        return {}
    elif malformed_type == "extra_garbage":
        return {
            "garbage_field": "x" * 5000,
            "invalid": True,
            "nested": {"deep": {"data": [1, 2, 3]}},
        }
    else:  # invalid_date
        return {
            "date": "not-a-date",
            "forecast_j_1": 55000.0,
            "forecast_j": 55000.0,
        }


# ─────────────────────────────────────────────
# User behavior
# ─────────────────────────────────────────────

class ElectricityPredictorUser(HttpUser):
    """Simulates a user of the EDF/RTE Predictor API."""

    wait_time = between(1, 3)

    def on_start(self):
        """Called when a virtual user starts running."""
        self.session_start = time.time()
        self.request_count = 0
        logger.debug(f"User started at {datetime.now().isoformat()}")

    def on_stop(self):
        """Called when a virtual user stops."""
        duration = time.time() - self.session_start
        logger.debug(f"User stopped after {duration:.1f}s, {self.request_count} requests")

    @task(8)
    def post_prediction_request(self):
        """Send a valid prediction request to POST /predict."""
        payload = generate_valid_payload()
        headers = {"Content-Type": "application/json"}

        with self.client.post(
            "/predict",
            json=payload,
            headers=headers,
            catch_response=True,
            name="/predict [valid]",
        ) as response:
            self.request_count += 1
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "prediction_mw" in data and data.get("status") == "success":
                        response.success()
                    else:
                        response.failure(f"Unexpected response format: {data}")
                except Exception as e:
                    response.failure(f"JSON parse error: {e}")
            elif response.status_code == 503:
                response.failure("Service unavailable — model not loaded")
            else:
                response.failure(
                    f"Status {response.status_code}: {response.text[:200]}"
                )

    @task(1)
    def post_malformed_request(self):
        """Send a malformed request to test error handling."""
        payload = generate_malformed_payload()
        headers = {"Content-Type": "application/json"}

        with self.client.post(
            "/predict",
            json=payload,
            headers=headers,
            catch_response=True,
            name="/predict [malformed]",
        ) as response:
            self.request_count += 1
            # Malformed requests should return 4xx errors — that's expected behavior
            if response.status_code in (400, 422):
                response.success()  # Error handling works correctly
            elif response.status_code == 200:
                response.failure("Malformed request should not succeed")
            else:
                response.failure(
                    f"Unexpected status {response.status_code} for malformed request"
                )

    @task(1)
    def check_health(self):
        """Simulate health probes checking the API health status."""
        with self.client.get(
            "/health",
            catch_response=True,
            name="/health",
        ) as response:
            self.request_count += 1
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Health check failed: {response.status_code}")

    @task(1)
    def fetch_metrics(self):
        """Simulate Prometheus scraping the metrics endpoint."""
        with self.client.get(
            "/metrics",
            catch_response=True,
            name="/metrics",
        ) as response:
            self.request_count += 1
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Metrics fetch failed: {response.status_code}")

    @task(1)
    def post_missing_fields(self):
        """Send a request with only the date field (all others use defaults)."""
        payload = {"date": "2025-03-15"}
        headers = {"Content-Type": "application/json"}

        with self.client.post(
            "/predict",
            json=payload,
            headers=headers,
            catch_response=True,
            name="/predict [minimal]",
        ) as response:
            self.request_count += 1
            if response.status_code in (200, 422):
                response.success()
            else:
                response.failure(
                    f"Minimal request returned {response.status_code}: {response.text[:200]}"
                )


# ─────────────────────────────────────────────
# Load shape — automatic ramp-up to 1000 users
# ─────────────────────────────────────────────

class StepLoadShape(LoadTestShape):
    """
    Step load shape: ramp up to 1000 users in incremental steps.

    Steps:
        1.  0-30s   →  50 users  (warm-up)
        2.  30-60s  → 100 users
        3.  60-90s  → 200 users
        4.  90-120s → 500 users
        5. 120-180s → 1000 users (peak load)
        6. 180-240s → 1000 users (sustained peak)
        7. 240-270s →  100 users (scale down)
        8. 270-300s →   10 users (cool down)
        9.    >300s →  stop
    """

    stages = [
        {"duration": 30, "users": 50, "spawn_rate": 10},
        {"duration": 60, "users": 100, "spawn_rate": 10},
        {"duration": 90, "users": 200, "spawn_rate": 20},
        {"duration": 120, "users": 500, "spawn_rate": 30},
        {"duration": 180, "users": 1000, "spawn_rate": 50},
        {"duration": 240, "users": 1000, "spawn_rate": 50},
        {"duration": 270, "users": 100, "spawn_rate": 50},
        {"duration": 300, "users": 10, "spawn_rate": 50},
    ]

    def tick(self):
        """Return (user_count, spawn_rate) tuple or None to stop."""
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                return (stage["users"], stage["spawn_rate"])

        # Test complete
        return None
