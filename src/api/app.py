import os
import time
import joblib
import numpy as np

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from prometheus_client import (
    Counter,
    Histogram,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST,
)
from fastapi.responses import Response


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


# 4. Input / output schemas
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


class PredictResponse(BaseModel):
    date: str
    prediction_mw: float
    status: str
    model_used: str
    latency_sec: float


# 5. API endpoints
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

        # Predict daily average consumption in MW
        prediction = float(model.predict(X_scaled)[0])

        latency = time.time() - start_time

        INFERENCE_LATENCY.observe(latency)
        PREDICTED_CONSUMPTION.set(prediction)
        REQUEST_COUNT.labels("POST", "/predict", "200").inc()

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
