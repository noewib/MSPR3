import os
import time
import datetime
import joblib
import pandas as pd
import numpy as np
from typing import Optional
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
    title="RTE/EDF Electricity Consumption Predictor API",
    description="API standardisée pour l'inférence en temps réel de la consommation électrique nationale.",
    version="1.0.0",
)

# 2. Define Prometheus metrics
REQUEST_COUNT = Counter(
    "http_requests_total", "Total HTTP Requests", ["method", "endpoint", "http_status"]
)
INFERENCE_LATENCY = Histogram(
    "inference_latency_seconds",
    "Latency of inference endpoint in seconds",
    buckets=[0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0],
)
PREDICTED_CONSUMPTION = Gauge(
    "predicted_consumption_megawatts",
    "Value of the electricity consumption predicted in MW",
)

# 3. Model Loading
MODEL_PATH = "models/best_model.joblib"
PIPELINE_PATH = "models/data_pipeline.joblib"

model = None
pipeline = None


def load_model_and_pipeline():
    global model, pipeline
    if os.path.exists(MODEL_PATH) and os.path.exists(PIPELINE_PATH):
        model = joblib.load(MODEL_PATH)
        pipeline = joblib.load(PIPELINE_PATH)
        print("Model and pipeline successfully loaded.")
    else:
        print("Model or pipeline not found. Training a quick default model...")
        # Auto-train a fast model on startup to ensure API works
        from src.models.train_evaluate import main as run_training

        try:
            run_training()
            model = joblib.load(MODEL_PATH)
            pipeline = joblib.load(PIPELINE_PATH)
            print("Auto-training completed and model loaded.")
        except Exception as e:
            print(f"Error auto-training: {e}")


@app.on_event("startup")
def startup_event():
    load_model_and_pipeline()


# 4. Input/Output Schemas
class PredictRequest(BaseModel):
    datetime_str: str = Field(
        ...,
        alias="datetime",
        description="Format ISO 8601 (ex: '2026-05-27T18:30:00')",
        examples=["2026-05-27T18:30:00"],
    )
    temperature: float = Field(
        ...,
        description="Température nationale moyenne en degrés Celsius",
        examples=[12.5],
    )
    # Lags and rolling metrics are optional. If not provided, we fill them with smart defaults/estimations.
    lag_24h: Optional[float] = Field(None, description="Consommation à t-24h (MW)")
    lag_48h: Optional[float] = Field(None, description="Consommation à t-48h (MW)")
    lag_7d: Optional[float] = Field(None, description="Consommation à t-7 jours (MW)")
    temp_roll_mean_3h: Optional[float] = Field(
        None, description="Moyenne glissante 3h de la température"
    )
    temp_roll_mean_6h: Optional[float] = Field(
        None, description="Moyenne glissante 6h de la température"
    )


class PredictResponse(BaseModel):
    datetime: str
    prediction_mw: float
    status: str
    model_used: str
    latency_sec: float


# 5. API Endpoints
@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    start_time = time.time()

    # Check if model is loaded
    if model is None or pipeline is None:
        REQUEST_COUNT.labels(
            method="POST", endpoint="/predict", http_status="503"
        ).inc()
        raise HTTPException(
            status_code=503,
            detail="Model is not initialized. Please train the model first.",
        )

    try:
        # Parse datetime
        dt = pd.to_datetime(request.datetime_str)
    except Exception:
        REQUEST_COUNT.labels(
            method="POST", endpoint="/predict", http_status="400"
        ).inc()
        raise HTTPException(
            status_code=400,
            detail="Invalid datetime format. Please use ISO 8601 format.",
        )

    try:
        # Fill missing features with reasonable defaults if not provided
        # 1. Base consumption around 55000 MW if lags not provided
        lag_24h = request.lag_24h if request.lag_24h is not None else 55000.0
        lag_48h = request.lag_48h if request.lag_48h is not None else 55000.0
        lag_7d = request.lag_7d if request.lag_7d is not None else 55000.0

        # 2. Rolling temperatures
        temp_3h = (
            request.temp_roll_mean_3h
            if request.temp_roll_mean_3h is not None
            else request.temperature
        )
        temp_6h = (
            request.temp_roll_mean_6h
            if request.temp_roll_mean_6h is not None
            else request.temperature
        )

        # Build single-row DataFrame for scaling & transformation
        input_data = pd.DataFrame(
            [
                {
                    "datetime": dt,
                    "temperature": request.temperature,
                    "consommation": 0.0,  # Placeholder target
                }
            ]
        )

        # Run pipeline feature engineering (it expects the columns but we will override lags manually)
        df_feat = pipeline.feature_engineering(input_data, is_training=False)

        # Force the user-specified or defaulted lags/rolling
        df_feat["lag_24h"] = lag_24h
        df_feat["lag_48h"] = lag_48h
        df_feat["lag_7d"] = lag_7d
        df_feat["temp_roll_mean_3h"] = temp_3h
        df_feat["temp_roll_mean_6h"] = temp_6h

        # Apply scaler
        X = pipeline.scaler.transform(df_feat[pipeline.feature_cols].values)

        # Inference
        pred = float(model.predict(X)[0])

        # Record metrics
        latency = time.time() - start_time
        INFERENCE_LATENCY.observe(latency)
        PREDICTED_CONSUMPTION.set(pred)
        REQUEST_COUNT.labels(
            method="POST", endpoint="/predict", http_status="200"
        ).inc()

        # Return response
        return PredictResponse(
            datetime=str(dt),
            prediction_mw=np.round(pred, 1),
            status="success",
            model_used=model.__class__.__name__,
            latency_sec=latency,
        )

    except Exception as e:
        REQUEST_COUNT.labels(
            method="POST", endpoint="/predict", http_status="500"
        ).inc()
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")


@app.get("/metrics")
def metrics():
    # Record a hit to /metrics
    REQUEST_COUNT.labels(method="GET", endpoint="/metrics", http_status="200").inc()
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/health")
def health():
    REQUEST_COUNT.labels(method="GET", endpoint="/health", http_status="200").inc()
    if model is None or pipeline is None:
        return {"status": "unhealthy", "reason": "model_not_loaded"}
    return {"status": "ok"}
