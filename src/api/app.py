import os
import csv
import json
import time
import asyncio
import joblib
import numpy as np
import warnings

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response, HTMLResponse, FileResponse
from pydantic import BaseModel, Field
from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

# Suppress sklearn version warnings for model loading
warnings.filterwarnings("ignore", category=UserWarning)


# 1. Initialize FastAPI app
app = FastAPI(
    title="RTE/EDF Daily Electricity Consumption Predictor API",
    description="API pour prédire la consommation électrique moyenne journalière en MW à partir des données RTE Eco2mix.",
    version="2.0.0",
)


# 2. Prometheus metrics
REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP Requests", ["method", "endpoint", "http_status"]
)

INFERENCE_LATENCY = Histogram(
    "inference_latency_seconds",
    "Latency of inference endpoint in seconds",
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0],
)

PREDICTED_CONSUMPTION = Gauge(
    "predicted_daily_consumption_mw",
    "Predicted daily average electricity consumption in MW",
)

# Internal tracking for dashboard
_metrics_history = {
    "timestamps": [],
    "request_counts": [],
    "latencies": [],
    "predictions": [],
}
_startup_time = time.time()
_load_test_results = []


# 3. Model loading
MODEL_PATH = "models/best_model.joblib"
PIPELINE_PATH = "models/data_pipeline.joblib"

model = None
pipeline = None


def load_model_and_pipeline():
    global model, pipeline

    if not os.path.exists(MODEL_PATH) or not os.path.exists(PIPELINE_PATH):
        raise FileNotFoundError(
            "Model or pipeline not found. Run: python -m src.models.train_evaluate"
        )

    model = joblib.load(MODEL_PATH)
    pipeline = joblib.load(PIPELINE_PATH)
    print("Model and pipeline successfully loaded.")


@app.on_event("startup")
def startup_event():
    try:
        load_model_and_pipeline()
    except Exception as e:
        print(f"Startup warning: {e}")


# 4. Mount static files for dashboard
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# 5. Input / output schemas
class PredictRequest(BaseModel):
    date: str = Field(
        ..., description="Prediction date, format YYYY-MM-DD", example="2025-01-15"
    )

    forecast_j_1: float = Field(
        55000.0, description="RTE forecast J-1, daily average MW"
    )
    forecast_j: float = Field(55000.0, description="RTE forecast J, daily average MW")

    lag_1d: float = Field(55000.0, description="Consumption one day before")
    lag_7d: float = Field(55000.0, description="Consumption seven days before")
    lag_14d: float = Field(55000.0, description="Consumption fourteen days before")
    rolling_mean_7d: float = Field(
        55000.0, description="Rolling average over previous seven days"
    )
    rolling_mean_30d: float = Field(
        55000.0, description="Rolling average over previous thirty days"
    )

    fioul: float = 0.0
    coal: float = 0.0
    gas: float = 0.0
    nuclear: float = 0.0
    wind: float = 0.0
    solar: float = 0.0
    hydraulic: float = 0.0
    pumping: float = 0.0
    bioenergy: float = 0.0
    physical_exchanges: float = 0.0
    co2_rate: float = 0.0
    model_name: str | None = Field(None, description="Optional model to use (e.g. 'RandomForest', 'DecisionTree'). Uses best_model if None.")


class PredictResponse(BaseModel):
    date: str
    prediction_mw: float
    status: str
    model_used: str
    latency_sec: float


class LoadTestConfig(BaseModel):
    num_requests: int = Field(100, description="Number of total requests to send")
    concurrency: int = Field(10, description="Number of concurrent workers")


class LoadTestResult(BaseModel):
    total_requests: int
    successful: int
    failed: int
    avg_response_time_ms: float
    min_response_time_ms: float
    max_response_time_ms: float
    p50_ms: float
    p95_ms: float
    p99_ms: float
    requests_per_second: float
    error_rate_percent: float
    duration_seconds: float
    response_times: list
    errors: list


# 6. Dashboard root route
@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    """Serve the main dashboard page."""
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(
        content="<h1>Dashboard not found</h1><p>Static files missing. Check src/api/static/</p>",
        status_code=404,
    )


# 7. Original API endpoints
@app.get("/health")
def health():
    REQUEST_COUNT.labels("GET", "/health", "200").inc()
    return {"status": "ok"}


@app.get("/ready")
def ready():
    if model is None or pipeline is None:
        REQUEST_COUNT.labels("GET", "/ready", "503").inc()
        return {"status": "unhealthy", "reason": "model_not_loaded"}

    REQUEST_COUNT.labels("GET", "/ready", "200").inc()
    return {"status": "ready"}


@app.get("/metrics")
def metrics():
    REQUEST_COUNT.labels("GET", "/metrics", "200").inc()
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    global model, pipeline

    if model is None or pipeline is None:
        try:
            load_model_and_pipeline()
        except Exception as e:
            REQUEST_COUNT.labels("POST", "/predict", "503").inc()
            raise HTTPException(status_code=503, detail=str(e))

    start_time = time.time()

    try:
        payload = request.dict()

        # Build one inference row with same features as training
        X_df = pipeline.prepare_inference_row(payload)

        # Apply scaler saved during training
        X_scaled = pipeline.scaler.transform(X_df.values)

        # Select model to use
        model_to_use = model
        model_used_name = model.__class__.__name__

        if request.model_name:
            specific_model_path = f"models/model_{request.model_name}.joblib"
            if os.path.exists(specific_model_path):
                model_to_use = joblib.load(specific_model_path)
                model_used_name = request.model_name
            else:
                raise ValueError(f"Model '{request.model_name}' not found. Available models: RandomForest, DecisionTree, KNeighbors, RBFN.")

        # Predict daily average consumption in MW
        prediction = float(model_to_use.predict(X_scaled)[0])

        latency = time.time() - start_time

        INFERENCE_LATENCY.observe(latency)
        PREDICTED_CONSUMPTION.set(prediction)
        REQUEST_COUNT.labels("POST", "/predict", "200").inc()

        # Track for dashboard
        _metrics_history["timestamps"].append(time.time())
        _metrics_history["request_counts"].append(
            len(_metrics_history["timestamps"])
        )
        _metrics_history["latencies"].append(round(latency * 1000, 2))
        _metrics_history["predictions"].append(round(prediction, 2))

        # Keep only last 200 data points
        for key in _metrics_history:
            if len(_metrics_history[key]) > 200:
                _metrics_history[key] = _metrics_history[key][-200:]

        return PredictResponse(
            date=request.date,
            prediction_mw=round(prediction, 2),
            status="success",
            model_used=model.__class__.__name__,
            latency_sec=round(latency, 6),
        )

    except ValueError as e:
        REQUEST_COUNT.labels("POST", "/predict", "400").inc()
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        REQUEST_COUNT.labels("POST", "/predict", "500").inc()
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")


# 8. Dashboard API endpoints
@app.get("/api/metrics-json")
def metrics_json():
    """Return Prometheus metrics as JSON for the dashboard charts."""
    uptime = round(time.time() - _startup_time, 1)

    return {
        "uptime_seconds": uptime,
        "history": {
            "timestamps": _metrics_history["timestamps"][-50:],
            "request_counts": _metrics_history["request_counts"][-50:],
            "latencies": _metrics_history["latencies"][-50:],
            "predictions": _metrics_history["predictions"][-50:],
        },
        "summary": {
            "total_requests": len(_metrics_history["timestamps"]),
            "avg_latency_ms": round(
                sum(_metrics_history["latencies"]) / max(len(_metrics_history["latencies"]), 1), 2
            ),
            "last_prediction": (
                _metrics_history["predictions"][-1]
                if _metrics_history["predictions"]
                else None
            ),
            "model_loaded": model is not None,
        },
    }


@app.get("/api/model-stats")
def model_stats():
    """Return model training statistics for the dashboard."""
    result = {"models": {}, "metadata": {}, "champion": None}

    # Load training metrics
    mlflow_path = "models/mlflow_logs.json"
    if os.path.exists(mlflow_path):
        with open(mlflow_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            models_list = []
            for name, metrics in data.items():
                models_list.append({
                    "name": name,
                    "r2": metrics.get("R2"),
                    "rmse": metrics.get("RMSE_MW"),
                    "mape": metrics.get("MAPE", 0) * 100,
                    "accuracy_5pct": metrics.get("Accuracy_5pct", 0) * 100,
                    "training_time": f"{metrics.get('Train_Time_sec', 0):.3f}s"
                })
            result["models"] = models_list

    # Load training metadata
    metadata_path = "models/training_metadata.json"
    if os.path.exists(metadata_path):
        with open(metadata_path, "r", encoding="utf-8") as f:
            metadata = json.load(f)
            result["metadata"] = metadata
            result["champion"] = metadata.get("best_model", None)

    return result


@app.get("/api/predictions-history")
def predictions_history():
    """Return test predictions for the ML results chart."""
    csv_path = "models/test_predictions.csv"
    if not os.path.exists(csv_path):
        return {"predictions": []}

    predictions = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= 200:  # Limit to 200 points for chart performance
                break
            predictions.append({
                "date": row.get("date", ""),
                "actual": float(row.get("y_true_mw", 0)),
                "predicted": float(row.get("y_pred_mw", 0)),
                "error": float(row.get("absolute_error_mw", 0)),
            })

    return {"predictions": predictions}


@app.get("/api/drift-report")
def drift_report():
    """Return data drift analysis report."""
    drift_path = "models/drift_report.json"
    if not os.path.exists(drift_path):
        return {"error": "Drift report not found"}

    with open(drift_path, "r", encoding="utf-8") as f:
        return json.load(f)


@app.post("/api/load-test", response_model=LoadTestResult)
async def run_load_test(config: LoadTestConfig):
    """Run an integrated load test against the API itself."""
    import concurrent.futures
    import random

    results = {
        "response_times": [],
        "errors": [],
        "status_codes": [],
    }

    def make_request(request_id):
        """Send a single prediction request."""
        import requests as req

        payload = {
            "date": f"2025-{random.randint(1,12):02d}-{random.randint(1,28):02d}",
            "forecast_j_1": round(random.uniform(40000, 70000), 1),
            "forecast_j": round(random.uniform(40000, 70000), 1),
            "lag_1d": round(random.uniform(40000, 70000), 1),
            "lag_7d": round(random.uniform(40000, 70000), 1),
            "lag_14d": round(random.uniform(40000, 70000), 1),
            "rolling_mean_7d": round(random.uniform(40000, 70000), 1),
            "rolling_mean_30d": round(random.uniform(45000, 65000), 1),
            "nuclear": round(random.uniform(30000, 45000), 1),
            "wind": round(random.uniform(1000, 15000), 1),
            "solar": round(random.uniform(0, 10000), 1),
            "gas": round(random.uniform(2000, 8000), 1),
            "hydraulic": round(random.uniform(5000, 15000), 1),
        }

        start = time.time()
        try:
            resp = req.post(
                "http://127.0.0.1:8000/predict",
                json=payload,
                timeout=10,
            )
            elapsed = (time.time() - start) * 1000
            return {
                "time_ms": round(elapsed, 2),
                "status": resp.status_code,
                "error": None if resp.status_code == 200 else resp.text[:100],
            }
        except Exception as e:
            elapsed = (time.time() - start) * 1000
            return {
                "time_ms": round(elapsed, 2),
                "status": 0,
                "error": str(e)[:100],
            }

    # Run load test in thread pool
    overall_start = time.time()

    loop = asyncio.get_event_loop()
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=config.concurrency
    ) as executor:
        futures = [
            loop.run_in_executor(executor, make_request, i)
            for i in range(config.num_requests)
        ]
        task_results = await asyncio.gather(*futures)

    overall_duration = time.time() - overall_start

    # Aggregate results
    response_times = [r["time_ms"] for r in task_results]
    errors = [r["error"] for r in task_results if r["error"] is not None]
    successful = sum(1 for r in task_results if r["status"] == 200)
    failed = len(task_results) - successful

    sorted_times = sorted(response_times)
    n = len(sorted_times)

    result = LoadTestResult(
        total_requests=config.num_requests,
        successful=successful,
        failed=failed,
        avg_response_time_ms=round(sum(response_times) / max(n, 1), 2),
        min_response_time_ms=round(min(response_times) if response_times else 0, 2),
        max_response_time_ms=round(max(response_times) if response_times else 0, 2),
        p50_ms=round(sorted_times[n // 2] if n > 0 else 0, 2),
        p95_ms=round(sorted_times[int(n * 0.95)] if n > 0 else 0, 2),
        p99_ms=round(sorted_times[int(n * 0.99)] if n > 0 else 0, 2),
        requests_per_second=round(config.num_requests / max(overall_duration, 0.001), 2),
        error_rate_percent=round(failed / max(config.num_requests, 1) * 100, 2),
        duration_seconds=round(overall_duration, 2),
        response_times=response_times[:500],  # Limit for JSON response size
        errors=errors[:20],
    )

    # Save to history
    _load_test_results.append({
        "timestamp": time.time(),
        "config": config.dict(),
        "summary": {
            "total": result.total_requests,
            "successful": result.successful,
            "failed": result.failed,
            "avg_ms": result.avg_response_time_ms,
            "p95_ms": result.p95_ms,
            "rps": result.requests_per_second,
            "error_rate": result.error_rate_percent,
        },
    })

    return result


@app.get("/api/load-test-history")
def load_test_history():
    """Return history of load test runs."""
    return {"history": _load_test_results[-20:]}
