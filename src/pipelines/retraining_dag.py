from datetime import datetime, timedelta
import os
import joblib
import pandas as pd
import numpy as np

# In a real Airflow environment, we import DAG and Operators:
# from airflow import DAG
# from airflow.operators.python import PythonOperator


# Mock DAG class for environment safety & testing without full Airflow installation
class MockDAG:
    def __init__(self, dag_id, default_args, schedule_interval):
        self.dag_id = dag_id
        self.default_args = default_args
        self.schedule_interval = schedule_interval


# Mock PythonOperator class
class MockPythonOperator:
    def __init__(self, task_id, python_callable, op_kwargs=None, dag=None):
        self.task_id = task_id
        self.python_callable = python_callable
        self.op_kwargs = op_kwargs or {}


# Default arguments for Airflow
default_args = {
    "owner": "mlops_team",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
    "email": ["mlops-alerts@edf.fr"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

# Define dummy DAG if Airflow is not installed, otherwise use real DAG
try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator

    dag = DAG(
        "edf_consumption_predictor_retraining",
        default_args=default_args,
        description="Weekly automatic retraining and deployment of the electricity predictor.",
        schedule_interval="@weekly",
        catchup=False,
    )
except ImportError:
    # Fallback to Mock classes for local script verification
    DAG = MockDAG
    PythonOperator = MockPythonOperator

    dag = DAG(
        dag_id="edf_consumption_predictor_retraining",
        default_args=default_args,
        schedule_interval="@weekly",
    )


def extract_and_prepare_data(**kwargs):
    """Task 1: Fetch recent historical data and engineer features."""
    print("Executing Task 1: Extract and Prepare Data...")
    from src.data.data_pipeline import DataPipeline

    pipeline = DataPipeline()
    # Ingest last 90 days of fresh data
    df = pipeline.generate_historical_data(days=90)

    # Save temp extraction file for next tasks
    os.makedirs("tmp", exist_ok=True)
    df.to_parquet("tmp/extracted_data.parquet")
    print("Fresh data extracted and saved to tmp/extracted_data.parquet")
    return "tmp/extracted_data.parquet"


def train_challenger(**kwargs):
    """Task 2: Train a challenger model on the new dataset."""
    print("Executing Task 2: Train Challenger Model...")
    from src.data.data_pipeline import DataPipeline
    from src.models.custom_rbfn import RadialBasisFunctionNetwork
    from sklearn.ensemble import RandomForestRegressor

    # Load dataset prepared in Task 1
    df = pd.read_parquet("tmp/extracted_data.parquet")

    pipeline = DataPipeline()
    X, y = pipeline.fit_transform(df)

    # Train the chosen champion architecture (e.g. RandomForest)
    # with slightly fresh hyperparameter tuning if needed
    challenger_model = RandomForestRegressor(
        n_estimators=40, max_depth=12, random_state=42
    )
    challenger_model.fit(X, y)

    # Save challenger artifacts
    os.makedirs("tmp", exist_ok=True)
    joblib.dump(challenger_model, "tmp/challenger_model.joblib")
    joblib.dump(pipeline, "tmp/challenger_pipeline.joblib")
    print("Challenger model trained and cached in tmp/")
    return "tmp/challenger_model.joblib"


def evaluate_and_compare(**kwargs):
    """Task 3: Compare Challenger performance against Champion on test set."""
    print("Executing Task 3: Evaluating Champion vs Challenger...")
    from sklearn.metrics import mean_absolute_percentage_error

    # 1. Load test dataset (eg. the last 15 days of the fresh dataset)
    df = pd.read_parquet("tmp/extracted_data.parquet")
    split_idx = int(len(df) * 0.85)
    test_df = df.iloc[split_idx:]

    # 2. Load Champion (production model)
    champion_model_path = "models/best_model.joblib"
    champion_pipeline_path = "models/data_pipeline.joblib"

    if not os.path.exists(champion_model_path):
        print("No champion model exists. Automatically promoting Challenger.")
        promote_challenger()
        return "Challenger promoted directly (No previous champion)."

    champion = joblib.load(champion_model_path)
    champion_pipeline = joblib.load(champion_pipeline_path)

    # 3. Load Challenger
    challenger = joblib.load("tmp/challenger_model.joblib")
    challenger_pipeline = joblib.load("tmp/challenger_pipeline.joblib")

    # 4. Predict and compute metrics
    y_true = test_df["consommation"].values

    # Champion evaluation
    X_champ = champion_pipeline.transform(test_df)
    pred_champ = champion.predict(X_champ)
    mape_champ = mean_absolute_percentage_error(y_true, pred_champ)

    # Challenger evaluation
    X_chal = challenger_pipeline.transform(test_df)
    pred_chal = challenger.predict(X_chal)
    mape_chal = mean_absolute_percentage_error(y_true, pred_chal)

    print(f"Champion MAPE: {mape_champ*100:.3f}%")
    print(f"Challenger MAPE: {mape_chal*100:.3f}%")

    # 5. Rule validation: challenger replaces champion only if MAPE is strictly lower
    # and under 5% (satisfying the business criticality limit)
    if mape_chal < mape_champ and mape_chal <= 0.05:
        print("Challenger performance is superior. Promoting Challenger to production.")
        promote_challenger()
        return (
            f"Promoted: Challenger ({mape_chal:.4f}) beat Champion ({mape_champ:.4f})."
        )
    else:
        print("Champion remains in production. Challenger rejected.")
        return f"Kept Champion: Champion ({mape_champ:.4f}) beat/tied Challenger ({mape_chal:.4f})."


def promote_challenger():
    """Helper to copy challenger artifacts to production paths."""
    os.makedirs("models", exist_ok=True)

    # Copy files
    import shutil

    shutil.copy("tmp/challenger_model.joblib", "models/best_model.joblib")
    shutil.copy("tmp/challenger_pipeline.joblib", "models/data_pipeline.joblib")
    print("Production best_model.joblib and data_pipeline.joblib successfully updated.")


# Instantiating the operators for the Airflow DAG
task_extract = PythonOperator(
    task_id="extract_and_prepare_data",
    python_callable=extract_and_prepare_data,
    dag=dag,
)

task_train_challenger = PythonOperator(
    task_id="train_challenger",
    python_callable=train_challenger,
    dag=dag,
)

task_evaluate_compare = PythonOperator(
    task_id="evaluate_and_compare",
    python_callable=evaluate_and_compare,
    dag=dag,
)

# Set dependencies
# In standard Airflow: task_extract >> task_train_challenger >> task_evaluate_compare
# We can represent it here:
if not isinstance(task_extract, MockPythonOperator):
    task_extract >> task_train_challenger >> task_evaluate_compare
else:
    print(
        "Mock DAG structure initialized: task_extract >> task_train_challenger >> task_evaluate_compare"
    )
