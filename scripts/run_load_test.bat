@echo off
echo ============================================================
echo === EDF/RTE Predictor — Test de Charge 1000 Utilisateurs ===
echo ============================================================
echo.
python scripts/run_load_test.py --users 1000 --duration 60 --ramp-up 10
echo.
pause
