#!/usr/bin/env python3
"""
Load Test Script — EDF/RTE Predictor API
Tests montée en charge 1000 utilisateurs + simulation de panne

Usage:
    python scripts/run_load_test.py --users 1000 --duration 60 --ramp-up 10
"""

import argparse
import json
import os
import random
import statistics
import sys
import threading
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta

try:
    import requests
except ImportError:
    print("ERROR: 'requests' package is required. Install with: pip install requests")
    sys.exit(1)


# ─────────────────────────────────────────────
# Realistic payload generator
# ─────────────────────────────────────────────

def generate_predict_payload(malformed=False):
    """Generate a realistic /predict payload matching PredictRequest schema."""
    if malformed:
        # Return various types of malformed payloads
        malformed_type = random.choice(["missing_fields", "bad_types", "empty", "garbage"])
        if malformed_type == "missing_fields":
            return {"date": "2025-01-15"}
        elif malformed_type == "bad_types":
            return {
                "date": 12345,
                "forecast_j_1": "not_a_number",
                "nuclear": None,
            }
        elif malformed_type == "empty":
            return {}
        else:
            return {"garbage": "!!!" * 100, "x": [1, 2, 3]}

    # Random date within 2024-2025 range
    base = datetime(2024, 1, 1)
    random_days = random.randint(0, 500)
    target_date = base + timedelta(days=random_days)

    # Seasonal consumption pattern (higher in winter)
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


# ─────────────────────────────────────────────
# Thread-safe metrics collector
# ─────────────────────────────────────────────

class MetricsCollector:
    """Thread-safe collector for load test metrics."""

    def __init__(self):
        self._lock = threading.Lock()
        self.response_times = []
        self.timestamps = []
        self.status_codes = defaultdict(int)
        self.errors = []
        self.request_count = 0
        self.start_time = None

    def record(self, elapsed, status_code, error=None, timestamp=None):
        with self._lock:
            self.request_count += 1
            self.response_times.append(elapsed)
            self.timestamps.append(timestamp or time.time())
            self.status_codes[status_code] += 1
            if error:
                self.errors.append({"time": time.time(), "error": str(error), "status": status_code})

    def get_summary(self):
        with self._lock:
            if not self.response_times:
                return {}
            sorted_rt = sorted(self.response_times)
            n = len(sorted_rt)
            return {
                "total_requests": self.request_count,
                "successful": sum(v for k, v in self.status_codes.items() if 200 <= k < 300),
                "failed": sum(v for k, v in self.status_codes.items() if k >= 400),
                "error_rate_pct": round(
                    sum(v for k, v in self.status_codes.items() if k >= 400) / max(n, 1) * 100, 2
                ),
                "avg_response_time_ms": round(statistics.mean(sorted_rt) * 1000, 2),
                "median_response_time_ms": round(statistics.median(sorted_rt) * 1000, 2),
                "min_response_time_ms": round(sorted_rt[0] * 1000, 2),
                "max_response_time_ms": round(sorted_rt[-1] * 1000, 2),
                "p90_ms": round(sorted_rt[int(n * 0.90)] * 1000, 2),
                "p95_ms": round(sorted_rt[int(n * 0.95)] * 1000, 2),
                "p99_ms": round(sorted_rt[min(int(n * 0.99), n - 1)] * 1000, 2),
                "std_dev_ms": round(statistics.stdev(sorted_rt) * 1000, 2) if n > 1 else 0,
                "status_codes": dict(self.status_codes),
                "total_errors": len(self.errors),
            }


# ─────────────────────────────────────────────
# Request senders
# ─────────────────────────────────────────────

def send_predict_request(host, collector, malformed=False):
    """Send a single /predict request and record metrics."""
    payload = generate_predict_payload(malformed=malformed)
    try:
        start = time.time()
        resp = requests.post(
            f"{host}/predict",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10,
        )
        elapsed = time.time() - start
        collector.record(elapsed, resp.status_code, timestamp=start)
    except requests.exceptions.RequestException as e:
        elapsed = time.time() - start
        collector.record(elapsed, 0, error=e, timestamp=start)


def send_health_request(host, collector):
    """Send a /health GET request."""
    try:
        start = time.time()
        resp = requests.get(f"{host}/health", timeout=5)
        elapsed = time.time() - start
        collector.record(elapsed, resp.status_code, timestamp=start)
    except requests.exceptions.RequestException as e:
        elapsed = time.time() - start
        collector.record(elapsed, 0, error=e, timestamp=start)


def send_metrics_request(host, collector):
    """Send a /metrics GET request."""
    try:
        start = time.time()
        resp = requests.get(f"{host}/metrics", timeout=5)
        elapsed = time.time() - start
        collector.record(elapsed, resp.status_code, timestamp=start)
    except requests.exceptions.RequestException as e:
        elapsed = time.time() - start
        collector.record(elapsed, 0, error=e, timestamp=start)


# ─────────────────────────────────────────────
# Test phases
# ─────────────────────────────────────────────

def phase_ramp_up(host, collector, max_users, ramp_up_seconds):
    """Phase 1: Gradually ramp up from 0 to max_users."""
    print(f"\n{'='*60}")
    print(f"  PHASE 1 — MONTÉE EN CHARGE (Ramp-Up)")
    print(f"  0 → {max_users} utilisateurs en {ramp_up_seconds}s")
    print(f"{'='*60}")

    steps = min(ramp_up_seconds, 10)
    users_per_step = max(1, max_users // steps)
    step_duration = ramp_up_seconds / steps

    for step in range(steps):
        current_users = min((step + 1) * users_per_step, max_users)
        print(f"  ↗ Step {step+1}/{steps}: {current_users} utilisateurs concurrents...")

        with ThreadPoolExecutor(max_workers=current_users) as executor:
            futures = []
            for _ in range(current_users):
                endpoint = random.choices(
                    ["predict", "health", "metrics"],
                    weights=[8, 1, 1],
                    k=1
                )[0]
                if endpoint == "predict":
                    futures.append(executor.submit(send_predict_request, host, collector))
                elif endpoint == "health":
                    futures.append(executor.submit(send_health_request, host, collector))
                else:
                    futures.append(executor.submit(send_metrics_request, host, collector))

            for f in as_completed(futures):
                f.result()

        time.sleep(max(0, step_duration - 0.1))

    print(f"  ✅ Ramp-up terminé — {collector.request_count} requêtes envoyées")


def phase_sustained_load(host, collector, max_users, duration_seconds):
    """Phase 2: Maintain max concurrent users for the duration."""
    print(f"\n{'='*60}")
    print(f"  PHASE 2 — CHARGE SOUTENUE")
    print(f"  {max_users} utilisateurs pendant {duration_seconds}s")
    print(f"{'='*60}")

    end_time = time.time() + duration_seconds
    batch = 0

    while time.time() < end_time:
        batch += 1
        remaining = end_time - time.time()
        if remaining <= 0:
            break

        batch_size = min(max_users, 200)  # Process in batches to avoid overwhelming the pool
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            futures = []
            for _ in range(batch_size):
                endpoint = random.choices(
                    ["predict", "health", "metrics"],
                    weights=[8, 1, 1],
                    k=1
                )[0]
                if endpoint == "predict":
                    futures.append(executor.submit(send_predict_request, host, collector))
                elif endpoint == "health":
                    futures.append(executor.submit(send_health_request, host, collector))
                else:
                    futures.append(executor.submit(send_metrics_request, host, collector))

            for f in as_completed(futures):
                f.result()

        if batch % 5 == 0:
            summary = collector.get_summary()
            elapsed_total = time.time() - collector.start_time
            rps = summary["total_requests"] / max(elapsed_total, 1)
            print(f"  📊 Batch {batch}: {summary['total_requests']} req | "
                  f"{rps:.1f} req/s | "
                  f"avg {summary['avg_response_time_ms']:.0f}ms | "
                  f"err {summary['error_rate_pct']:.1f}%")

        # Small pause between batches to simulate realistic intervals
        time.sleep(0.1)

    print(f"  ✅ Charge soutenue terminée — {collector.request_count} requêtes total")


def phase_failure_simulation(host, collector):
    """Phase 3: Burst of 500 malformed requests to test error handling."""
    print(f"\n{'='*60}")
    print(f"  PHASE 3 — SIMULATION DE PANNE")
    print(f"  500 requêtes malformées simultanées")
    print(f"{'='*60}")

    failure_collector = MetricsCollector()
    failure_collector.start_time = time.time()
    burst_size = 500

    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = [
            executor.submit(send_predict_request, host, failure_collector, malformed=True)
            for _ in range(burst_size)
        ]
        for f in as_completed(futures):
            f.result()

    summary = failure_collector.get_summary()
    print(f"  💥 Burst terminé: {summary.get('total_requests', 0)} requêtes")
    print(f"  📉 Codes de statut: {summary.get('status_codes', {})}")
    print(f"  ⏱️ Temps moyen: {summary.get('avg_response_time_ms', 0):.0f}ms")

    # Merge failure metrics into main collector
    with collector._lock:
        collector.response_times.extend(failure_collector.response_times)
        collector.timestamps.extend(failure_collector.timestamps)
        collector.request_count += failure_collector.request_count
        for k, v in failure_collector.status_codes.items():
            collector.status_codes[k] += v
        collector.errors.extend(failure_collector.errors)

    return failure_collector


def phase_recovery_test(host, collector, max_users):
    """Phase 4: Measure recovery time after failure burst."""
    print(f"\n{'='*60}")
    print(f"  PHASE 4 — TEST DE RÉCUPÉRATION")
    print(f"  Mesure du temps de retour à la normale")
    print(f"{'='*60}")

    recovery_start = time.time()
    recovery_times = []
    recovered = False
    check_count = 0
    max_checks = 50

    while check_count < max_checks:
        check_count += 1
        batch_times = []

        with ThreadPoolExecutor(max_workers=min(max_users, 50)) as executor:
            futures = []
            for _ in range(20):
                futures.append(executor.submit(send_predict_request, host, collector))

            for f in as_completed(futures):
                f.result()

        # Check last 20 response times
        with collector._lock:
            recent = collector.response_times[-20:]

        if recent:
            avg_recent = statistics.mean(recent) * 1000
            batch_times.append(avg_recent)
            recovery_times.append({
                "check": check_count,
                "avg_ms": round(avg_recent, 2),
                "time_since_failure": round(time.time() - recovery_start, 2),
            })

            if avg_recent < 500:
                recovered = True
                recovery_duration = time.time() - recovery_start
                print(f"  ✅ Récupération en {recovery_duration:.2f}s (avg: {avg_recent:.0f}ms)")
                break
            else:
                print(f"  ⏳ Check {check_count}: avg {avg_recent:.0f}ms — en cours de récupération...")

        time.sleep(0.2)

    if not recovered:
        recovery_duration = time.time() - recovery_start
        print(f"  ⚠️ Récupération non confirmée après {recovery_duration:.1f}s")

    return {
        "recovered": recovered,
        "recovery_time_seconds": round(time.time() - recovery_start, 2),
        "checks": recovery_times,
    }


# ─────────────────────────────────────────────
# Report generation
# ─────────────────────────────────────────────

def generate_json_report(summary, recovery_data, output_dir, test_config):
    """Generate JSON results file."""
    report = {
        "test_info": {
            "timestamp": datetime.now().isoformat(),
            "host": test_config["host"],
            "target_users": test_config["users"],
            "duration_seconds": test_config["duration"],
            "ramp_up_seconds": test_config["ramp_up"],
        },
        "metrics": summary,
        "recovery": recovery_data,
        "pass_fail": {
            "avg_response_time_lt_500ms": summary.get("avg_response_time_ms", 9999) < 500,
            "error_rate_lt_5pct": summary.get("error_rate_pct", 100) < 5,
            "p95_lt_2000ms": summary.get("p95_ms", 9999) < 2000,
            "recovery_lt_10s": recovery_data.get("recovery_time_seconds", 999) < 10,
        },
    }

    filepath = os.path.join(output_dir, "load_test_results.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"\n  📄 Rapport JSON : {filepath}")
    return report


def generate_html_report(collector, summary, recovery_data, output_dir, test_config):
    """Generate HTML report with Chart.js graphs."""

    # Prepare time-series data (bucket by second)
    if not collector.timestamps:
        time_series_labels = []
        time_series_rt = []
        time_series_rps = []
        time_series_errors = []
    else:
        t0 = min(collector.timestamps)
        max_t = max(collector.timestamps)
        buckets = defaultdict(list)
        error_buckets = defaultdict(int)

        with collector._lock:
            for i, ts in enumerate(collector.timestamps):
                sec = int(ts - t0)
                buckets[sec].append(collector.response_times[i] * 1000)
            for err in collector.errors:
                sec = int(err["time"] - t0)
                error_buckets[sec] += 1

        total_seconds = int(max_t - t0) + 1
        time_series_labels = list(range(total_seconds))
        time_series_rt = [
            round(statistics.mean(buckets[s]), 1) if s in buckets else 0
            for s in range(total_seconds)
        ]
        time_series_rps = [len(buckets.get(s, [])) for s in range(total_seconds)]
        time_series_errors = [error_buckets.get(s, 0) for s in range(total_seconds)]

    # Response time distribution histogram
    if collector.response_times:
        hist_data = [rt * 1000 for rt in collector.response_times]
        hist_bins = [0, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
        hist_counts = []
        for i in range(len(hist_bins) - 1):
            count = sum(1 for rt in hist_data if hist_bins[i] <= rt < hist_bins[i + 1])
            hist_counts.append(count)
        hist_counts.append(sum(1 for rt in hist_data if rt >= hist_bins[-1]))
        hist_labels = [f"{hist_bins[i]}-{hist_bins[i+1]}ms" for i in range(len(hist_bins) - 1)]
        hist_labels.append(f">{hist_bins[-1]}ms")
    else:
        hist_labels = []
        hist_counts = []

    # Pass/Fail results
    pf = {
        "avg_rt": summary.get("avg_response_time_ms", 9999) < 500,
        "error_rate": summary.get("error_rate_pct", 100) < 5,
        "p95": summary.get("p95_ms", 9999) < 2000,
        "recovery": recovery_data.get("recovery_time_seconds", 999) < 10,
    }

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rapport de Test de Charge — EDF/RTE Predictor</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background: #0a0e1a;
            color: #e0e0e0;
            padding: 2rem;
            line-height: 1.6;
        }}
        .header {{
            text-align: center;
            margin-bottom: 2rem;
            padding: 2rem;
            background: linear-gradient(135deg, #1a1f35, #0d1117);
            border-radius: 16px;
            border: 1px solid #30363d;
        }}
        .header h1 {{ color: #58a6ff; font-size: 1.8rem; margin-bottom: 0.5rem; }}
        .header p {{ color: #8b949e; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; margin-bottom: 2rem; }}
        .metric-card {{
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
        }}
        .metric-card .value {{ font-size: 2rem; font-weight: 700; color: #58a6ff; }}
        .metric-card .label {{ color: #8b949e; font-size: 0.85rem; margin-top: 0.5rem; }}
        .chart-card {{
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }}
        .chart-card h3 {{ color: #58a6ff; margin-bottom: 1rem; }}
        .pass {{ color: #3fb950; }}
        .fail {{ color: #f85149; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 1rem;
        }}
        th, td {{
            padding: 0.75rem 1rem;
            text-align: left;
            border-bottom: 1px solid #30363d;
        }}
        th {{ color: #58a6ff; font-weight: 600; background: #0d1117; }}
        .badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
        }}
        .badge-pass {{ background: rgba(63,185,80,0.15); color: #3fb950; border: 1px solid #238636; }}
        .badge-fail {{ background: rgba(248,81,73,0.15); color: #f85149; border: 1px solid #da3633; }}
    </style>
</head>
<body>

    <div class="header">
        <h1>⚡ Rapport de Test de Charge</h1>
        <p>EDF/RTE Electricity Consumption Predictor API</p>
        <p>Généré le {datetime.now().strftime("%d/%m/%Y à %H:%M:%S")} |
           Hôte: {test_config['host']} |
           Utilisateurs: {test_config['users']} |
           Durée: {test_config['duration']}s</p>
    </div>

    <!-- Summary metrics -->
    <div class="grid">
        <div class="metric-card">
            <div class="value">{summary.get('total_requests', 0):,}</div>
            <div class="label">Requêtes totales</div>
        </div>
        <div class="metric-card">
            <div class="value">{summary.get('avg_response_time_ms', 0):.0f}ms</div>
            <div class="label">Temps de réponse moyen</div>
        </div>
        <div class="metric-card">
            <div class="value">{summary.get('p95_ms', 0):.0f}ms</div>
            <div class="label">P95 Latence</div>
        </div>
        <div class="metric-card">
            <div class="value">{summary.get('error_rate_pct', 0):.1f}%</div>
            <div class="label">Taux d'erreur</div>
        </div>
        <div class="metric-card">
            <div class="value">{recovery_data.get('recovery_time_seconds', 'N/A')}s</div>
            <div class="label">Temps de récupération</div>
        </div>
    </div>

    <!-- Pass / Fail -->
    <div class="chart-card">
        <h3>🎯 Critères de Validation</h3>
        <table>
            <thead>
                <tr><th>Critère</th><th>Seuil</th><th>Mesuré</th><th>Résultat</th></tr>
            </thead>
            <tbody>
                <tr>
                    <td>Temps de réponse moyen</td>
                    <td>&lt; 500 ms</td>
                    <td>{summary.get('avg_response_time_ms', 0):.1f} ms</td>
                    <td><span class="badge {'badge-pass' if pf['avg_rt'] else 'badge-fail'}">{'PASS' if pf['avg_rt'] else 'FAIL'}</span></td>
                </tr>
                <tr>
                    <td>Taux d'erreur</td>
                    <td>&lt; 5%</td>
                    <td>{summary.get('error_rate_pct', 0):.2f}%</td>
                    <td><span class="badge {'badge-pass' if pf['error_rate'] else 'badge-fail'}">{'PASS' if pf['error_rate'] else 'FAIL'}</span></td>
                </tr>
                <tr>
                    <td>Percentile 95</td>
                    <td>&lt; 2000 ms</td>
                    <td>{summary.get('p95_ms', 0):.1f} ms</td>
                    <td><span class="badge {'badge-pass' if pf['p95'] else 'badge-fail'}">{'PASS' if pf['p95'] else 'FAIL'}</span></td>
                </tr>
                <tr>
                    <td>Temps de récupération</td>
                    <td>&lt; 10 s</td>
                    <td>{recovery_data.get('recovery_time_seconds', 'N/A')} s</td>
                    <td><span class="badge {'badge-pass' if pf['recovery'] else 'badge-fail'}">{'PASS' if pf['recovery'] else 'FAIL'}</span></td>
                </tr>
            </tbody>
        </table>
    </div>

    <!-- Charts -->
    <div class="chart-card">
        <h3>📈 Temps de Réponse au Cours du Test</h3>
        <canvas id="responseTimeChart" height="80"></canvas>
    </div>

    <div class="chart-card">
        <h3>📊 Requêtes par Seconde</h3>
        <canvas id="rpsChart" height="80"></canvas>
    </div>

    <div class="chart-card">
        <h3>❌ Erreurs par Seconde</h3>
        <canvas id="errorChart" height="80"></canvas>
    </div>

    <div class="chart-card">
        <h3>📉 Distribution des Temps de Réponse</h3>
        <canvas id="histogramChart" height="80"></canvas>
    </div>

    <!-- Status codes table -->
    <div class="chart-card">
        <h3>📋 Répartition des Codes de Statut</h3>
        <table>
            <thead><tr><th>Code HTTP</th><th>Nombre</th><th>Pourcentage</th></tr></thead>
            <tbody>
                {''.join(
                    f'<tr><td>{code}</td><td>{count}</td><td>{count/max(summary.get("total_requests",1),1)*100:.1f}%</td></tr>'
                    for code, count in sorted(summary.get("status_codes", {}).items())
                )}
            </tbody>
        </table>
    </div>

    <script>
        const chartDefaults = {{
            responsive: true,
            plugins: {{ legend: {{ labels: {{ color: '#8b949e' }} }} }},
            scales: {{
                x: {{ ticks: {{ color: '#8b949e' }}, grid: {{ color: '#21262d' }} }},
                y: {{ ticks: {{ color: '#8b949e' }}, grid: {{ color: '#21262d' }} }}
            }}
        }};

        // Response Time Chart
        new Chart(document.getElementById('responseTimeChart'), {{
            type: 'line',
            data: {{
                labels: {json.dumps(time_series_labels)},
                datasets: [{{
                    label: 'Temps de réponse moyen (ms)',
                    data: {json.dumps(time_series_rt)},
                    borderColor: '#58a6ff',
                    backgroundColor: 'rgba(88,166,255,0.1)',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 0,
                }}]
            }},
            options: {{ ...chartDefaults }}
        }});

        // RPS Chart
        new Chart(document.getElementById('rpsChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(time_series_labels)},
                datasets: [{{
                    label: 'Requêtes/s',
                    data: {json.dumps(time_series_rps)},
                    backgroundColor: 'rgba(63,185,80,0.6)',
                    borderColor: '#3fb950',
                    borderWidth: 1,
                }}]
            }},
            options: {{ ...chartDefaults }}
        }});

        // Error Chart
        new Chart(document.getElementById('errorChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(time_series_labels)},
                datasets: [{{
                    label: 'Erreurs/s',
                    data: {json.dumps(time_series_errors)},
                    backgroundColor: 'rgba(248,81,73,0.6)',
                    borderColor: '#f85149',
                    borderWidth: 1,
                }}]
            }},
            options: {{ ...chartDefaults }}
        }});

        // Histogram
        new Chart(document.getElementById('histogramChart'), {{
            type: 'bar',
            data: {{
                labels: {json.dumps(hist_labels)},
                datasets: [{{
                    label: 'Nombre de requêtes',
                    data: {json.dumps(hist_counts)},
                    backgroundColor: [
                        'rgba(63,185,80,0.6)', 'rgba(63,185,80,0.6)',
                        'rgba(88,166,255,0.6)', 'rgba(88,166,255,0.6)',
                        'rgba(210,153,34,0.6)', 'rgba(210,153,34,0.6)',
                        'rgba(248,81,73,0.6)', 'rgba(248,81,73,0.6)',
                        'rgba(248,81,73,0.8)'
                    ],
                    borderWidth: 1,
                }}]
            }},
            options: {{ ...chartDefaults }}
        }});
    </script>

</body>
</html>"""

    filepath = os.path.join(output_dir, "load_test_report.html")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  📊 Rapport HTML : {filepath}")
    return filepath


# ─────────────────────────────────────────────
# Console summary
# ─────────────────────────────────────────────

def print_summary(summary, recovery_data):
    """Print final pass/fail summary to console."""
    print(f"\n{'='*60}")
    print(f"  RÉSULTATS FINAUX — TEST DE CHARGE")
    print(f"{'='*60}")

    avg_rt = summary.get("avg_response_time_ms", 9999)
    err_rate = summary.get("error_rate_pct", 100)
    p95 = summary.get("p95_ms", 9999)
    rec_time = recovery_data.get("recovery_time_seconds", 999)

    criteria = [
        ("Temps de réponse moyen < 500ms", avg_rt < 500, f"{avg_rt:.1f}ms"),
        ("Taux d'erreur < 5%", err_rate < 5, f"{err_rate:.2f}%"),
        ("P95 < 2000ms", p95 < 2000, f"{p95:.1f}ms"),
        ("Récupération < 10s", rec_time < 10, f"{rec_time:.2f}s"),
    ]

    all_pass = True
    for name, passed, value in criteria:
        icon = "✅ PASS" if passed else "❌ FAIL"
        if not passed:
            all_pass = False
        print(f"  {icon} | {name}: {value}")

    print(f"\n  {'='*56}")
    if all_pass:
        print(f"  🎉 RÉSULTAT GLOBAL : TOUS LES CRITÈRES SONT VALIDÉS")
    else:
        print(f"  ⚠️  RÉSULTAT GLOBAL : CERTAINS CRITÈRES ONT ÉCHOUÉ")
    print(f"  {'='*56}")

    print(f"\n  📊 Statistiques détaillées :")
    print(f"     Requêtes totales  : {summary.get('total_requests', 0):,}")
    print(f"     Réussies          : {summary.get('successful', 0):,}")
    print(f"     Échouées          : {summary.get('failed', 0):,}")
    print(f"     Temps min         : {summary.get('min_response_time_ms', 0):.1f}ms")
    print(f"     Temps médian      : {summary.get('median_response_time_ms', 0):.1f}ms")
    print(f"     Temps max         : {summary.get('max_response_time_ms', 0):.1f}ms")
    print(f"     P90               : {summary.get('p90_ms', 0):.1f}ms")
    print(f"     P99               : {summary.get('p99_ms', 0):.1f}ms")
    print(f"     Écart-type        : {summary.get('std_dev_ms', 0):.1f}ms")

    return all_pass


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Test de charge — EDF/RTE Electricity Consumption Predictor API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python scripts/run_load_test.py --users 100 --duration 30
  python scripts/run_load_test.py --host http://api.example.com --users 1000 --duration 120
        """,
    )
    parser.add_argument("--host", default="http://127.0.0.1:8000", help="URL de l'API (default: http://127.0.0.1:8000)")
    parser.add_argument("--users", type=int, default=1000, help="Nombre d'utilisateurs concurrents (default: 1000)")
    parser.add_argument("--duration", type=int, default=60, help="Durée du test en secondes (default: 60)")
    parser.add_argument("--ramp-up", type=int, default=10, help="Durée de montée en charge en secondes (default: 10)")
    parser.add_argument("--output-dir", default="scripts/load_test_results", help="Répertoire de sortie (default: scripts/load_test_results)")
    args = parser.parse_args()

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║   ⚡ EDF/RTE Predictor — Test de Charge                     ║
║   1000 utilisateurs simultanés + simulation de panne        ║
╚══════════════════════════════════════════════════════════════╝

  🎯 Hôte          : {args.host}
  👥 Utilisateurs   : {args.users}
  ⏱️  Durée          : {args.duration}s
  ↗️  Ramp-up        : {args.ramp_up}s
  📁 Sortie         : {args.output_dir}
""")

    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)

    # Check API availability
    print("  🔍 Vérification de la disponibilité de l'API...")
    try:
        resp = requests.get(f"{args.host}/health", timeout=5)
        if resp.status_code == 200:
            print(f"  ✅ API accessible ({args.host})")
        else:
            print(f"  ⚠️  API répond avec statut {resp.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"  ❌ Impossible de contacter l'API à {args.host}")
        print(f"     Lancez l'API d'abord : uvicorn src.api.app:app --host 0.0.0.0 --port 8000")
        sys.exit(1)

    # Initialize collector
    collector = MetricsCollector()
    collector.start_time = time.time()

    test_config = {
        "host": args.host,
        "users": args.users,
        "duration": args.duration,
        "ramp_up": args.ramp_up,
    }

    # Phase 1: Ramp-up
    phase_ramp_up(args.host, collector, args.users, args.ramp_up)

    # Phase 2: Sustained load
    phase_sustained_load(args.host, collector, args.users, args.duration)

    # Phase 3: Failure simulation
    phase_failure_simulation(args.host, collector)

    # Phase 4: Recovery test
    recovery_data = phase_recovery_test(args.host, collector, args.users)

    # Generate reports
    total_elapsed = time.time() - collector.start_time
    summary = collector.get_summary()
    summary["total_test_duration_seconds"] = round(total_elapsed, 2)

    print(f"\n{'='*60}")
    print(f"  GÉNÉRATION DES RAPPORTS")
    print(f"{'='*60}")

    report = generate_json_report(summary, recovery_data, args.output_dir, test_config)
    generate_html_report(collector, summary, recovery_data, args.output_dir, test_config)

    # Console summary
    all_pass = print_summary(summary, recovery_data)

    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
