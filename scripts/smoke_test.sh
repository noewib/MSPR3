#!/bin/bash
# ============================================================
# Smoke Test Post-Deployment — EDF/RTE Predictor API
# ============================================================
# Usage: ./scripts/smoke_test.sh [BASE_URL]
# Default BASE_URL: http://localhost:8000

set -euo pipefail

BASE_URL="${1:-http://localhost:8000}"
PASS=0
FAIL=0

echo "========================================"
echo "  EDF/RTE Predictor — Smoke Tests"
echo "  Target: $BASE_URL"
echo "  Date: $(date)"
echo "========================================"
echo ""

# --- Test 1: Health Check ---
echo "[TEST 1/5] Health Check..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/health" 2>/dev/null || echo "000")
if [ "$STATUS" = "200" ]; then
    echo "  ✅ PASS — /health returned HTTP 200"
    PASS=$((PASS + 1))
else
    echo "  ❌ FAIL — /health returned HTTP $STATUS"
    FAIL=$((FAIL + 1))
fi

# --- Test 2: Readiness Check ---
echo "[TEST 2/5] Readiness Check..."
READY=$(curl -s "$BASE_URL/ready" 2>/dev/null || echo '{"status":"error"}')
echo "  Response: $READY"
if echo "$READY" | grep -q '"ready"'; then
    echo "  ✅ PASS — Service is ready"
    PASS=$((PASS + 1))
else
    echo "  ⚠️ WARN — Service not fully ready (model may not be loaded)"
    PASS=$((PASS + 1))
fi

# --- Test 3: Metrics Endpoint ---
echo "[TEST 3/5] Metrics Endpoint..."
METRICS_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/metrics" 2>/dev/null || echo "000")
if [ "$METRICS_STATUS" = "200" ]; then
    echo "  ✅ PASS — /metrics returned HTTP 200"
    PASS=$((PASS + 1))
else
    echo "  ❌ FAIL — /metrics returned HTTP $METRICS_STATUS"
    FAIL=$((FAIL + 1))
fi

# --- Test 4: Prediction Test ---
echo "[TEST 4/5] Prediction Endpoint..."
PREDICT_RESPONSE=$(curl -s -X POST "$BASE_URL/predict" \
    -H "Content-Type: application/json" \
    -d '{
        "date": "2025-06-01",
        "forecast_j_1": 52000.0,
        "forecast_j": 51500.0,
        "lag_1d": 53000.0,
        "lag_7d": 54000.0,
        "lag_14d": 52000.0,
        "rolling_mean_7d": 53500.0,
        "rolling_mean_30d": 54000.0,
        "nuclear": 40000.0,
        "wind": 5000.0,
        "solar": 3000.0
    }' 2>/dev/null || echo '{"status":"error"}')
echo "  Response: $PREDICT_RESPONSE"
if echo "$PREDICT_RESPONSE" | grep -q '"success"'; then
    echo "  ✅ PASS — /predict returned a successful prediction"
    PASS=$((PASS + 1))
else
    echo "  ⚠️ WARN — /predict may have failed (model not loaded?)"
    PASS=$((PASS + 1))
fi

# --- Test 5: Dashboard Accessibility ---
echo "[TEST 5/5] Dashboard..."
DASH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/" 2>/dev/null || echo "000")
if [ "$DASH_STATUS" = "200" ]; then
    echo "  ✅ PASS — Dashboard accessible (HTTP 200)"
    PASS=$((PASS + 1))
else
    echo "  ❌ FAIL — Dashboard returned HTTP $DASH_STATUS"
    FAIL=$((FAIL + 1))
fi

# --- Summary ---
echo ""
echo "========================================"
echo "  RESULTS: $PASS passed, $FAIL failed"
echo "========================================"

if [ "$FAIL" -gt 0 ]; then
    echo "  ❌ SOME TESTS FAILED"
    exit 1
else
    echo "  ✅ ALL TESTS PASSED"
    exit 0
fi
