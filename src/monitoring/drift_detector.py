import os
import json
import numpy as np
import pandas as pd

# Try importing scipy and evidently, providing fallback statistical calculations if not present
try:
    from scipy.stats import ks_2samp
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

try:
    from evidently.report import Report
    from evidently.metric_preset import DataDriftPreset
    HAS_EVIDENTLY = True
except Exception:
    HAS_EVIDENTLY = False

class DriftDetector:
    def __init__(self, threshold_pvalue=0.05):
        self.threshold_pvalue = threshold_pvalue

    def calculate_drift(self, reference_df: pd.DataFrame, current_df: pd.DataFrame, features: list) -> dict:
        """
        Compare current (production) dataset with reference (training) dataset.
        Returns a dictionary summarizing drift for each feature.
        """
        drift_results = {}
        
        # Method 1: Evidently AI Report
        if HAS_EVIDENTLY:
            try:
                report = Report(metrics=[DataDriftPreset()])
                # Filter dataframes to relevant features for the report
                ref_sub = reference_df[features].copy()
                cur_sub = current_df[features].copy()
                
                report.run(reference_data=ref_sub, current_data=cur_sub)
                
                # Save HTML report
                os.makedirs("docs/monitoring", exist_ok=True)
                report.save_html("docs/monitoring/data_drift_report.html")
                print("Evidently AI HTML drift report saved to docs/monitoring/data_drift_report.html.")
            except Exception as e:
                print(f"Error generating Evidently report: {e}. Falling back to statistical tests.")
        
        # Method 2: Native Kolmogorov-Smirnov 2-sample test
        # (Standard non-parametric test comparing cumulative distributions)
        for feature in features:
            if feature not in reference_df.columns or feature not in current_df.columns:
                continue
                
            ref_data = reference_df[feature].dropna().values
            cur_data = current_df[feature].dropna().values
            
            if len(ref_data) == 0 or len(cur_data) == 0:
                drift_results[feature] = {
                    "drift_detected": False,
                    "method": "Insufficient data",
                    "p_value": 1.0
                }
                continue
                
            if HAS_SCIPY:
                # Run KS-test
                stat, p_val = ks_2samp(ref_data, cur_data)
                drift_detected = bool(p_val < self.threshold_pvalue)
                drift_results[feature] = {
                    "drift_detected": drift_detected,
                    "method": "Kolmogorov-Smirnov",
                    "statistic": float(stat),
                    "p_value": float(p_val)
                }
            else:
                # Basic Fallback check (mean and std deviations check)
                ref_mean, ref_std = np.mean(ref_data), np.std(ref_data)
                cur_mean, cur_std = np.mean(cur_data), np.std(cur_data)
                
                # Check if current mean is outside 2 standard deviations of reference
                mean_diff = abs(ref_mean - cur_mean)
                std_threshold = 2.0 * (ref_std if ref_std > 0 else 1.0)
                drift_detected = bool(mean_diff > std_threshold)
                
                drift_results[feature] = {
                    "drift_detected": drift_detected,
                    "method": "Mean-Std-Check",
                    "ref_mean": float(ref_mean),
                    "cur_mean": float(cur_mean),
                    "mean_diff": float(mean_diff)
                }
                
        return drift_results

def main():
    print("--- Running Data Drift Detection ---")
    from src.data.data_pipeline import DataPipeline
    
    # Instantiate pipeline
    pipeline = DataPipeline()
    features = ['temperature', 'consommation']
    
    # 1. Load baseline (reference) data: eg 3 months of historical data
    print("Generating reference data (training baseline)...")
    reference_df = pipeline.generate_historical_data(days=90)
    
    # 2. Simulate current (production) data
    # Scenario A: Nominal (no drift, similar temperatures)
    print("Generating nominal current data (similar distribution)...")
    current_nominal_df = pipeline.generate_historical_data(days=7)
    
    # Scenario B: Drifted (extreme weather event: +8 degrees constant offset)
    print("Generating drifted current data (extreme heatwave simulation)...")
    current_drifted_df = current_nominal_df.copy()
    current_drifted_df['temperature'] += 8.0
    # Recalculate consumption based on new temperatures (would drift too)
    current_drifted_df['consommation'] = current_drifted_df['consommation'] - (8.0 * 1800.0) # heating drops
    
    # Initialize detector
    detector = DriftDetector(threshold_pvalue=0.05)
    
    # Run comparison on Nominal Scenario
    print("\n[Scenario A] Checking Nominal data...")
    results_nominal = detector.calculate_drift(reference_df, current_nominal_df, features)
    print("Nominal Drift Results:")
    print(json.dumps(results_nominal, indent=2))
    
    # Run comparison on Drifted Scenario
    print("\n[Scenario B] Checking Heatwave (drifted) data...")
    results_drifted = detector.calculate_drift(reference_df, current_drifted_df, features)
    print("Drifted Drift Results:")
    print(json.dumps(results_drifted, indent=2))
    
    # Check for alerts
    drift_alert = any(res['drift_detected'] for res in results_drifted.values())
    if drift_alert:
        print("\n>>> ALERT: Data drift detected! Initiating alarm or triggering retraining. <<<")
    else:
        print("\n>>> System stable. No drift detected. <<<")
        
    # Save results to a monitoring JSON
    os.makedirs("models", exist_ok=True)
    with open("models/drift_report.json", "w") as f:
        json.dump({
            "timestamp": str(pd.Timestamp.now()),
            "nominal_scenario": results_nominal,
            "drifted_scenario": results_drifted
        }, f, indent=4)
    print("Drift reports written to models/drift_report.json.")

if __name__ == "__main__":
    main()
