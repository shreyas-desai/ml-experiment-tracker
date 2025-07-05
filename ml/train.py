import os
import mlflow
import pandas as pd
import joblib
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_percentage_error, root_mean_squared_error
from dotenv import load_dotenv
from ml.utils import get_snowflake_connection
from ml.feature_engineering import add_features  # new module

load_dotenv()

def fetch_features():
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    query = """
        SELECT date, cpi, interest_rate, unemployment_rate, gdp
        FROM FEATURE_STORE
        WHERE cpi IS NOT NULL
        ORDER BY date
    """
    cursor.execute(query)
    df = pd.DataFrame(cursor.fetchall(), columns=['ds', 'cpi', 'interest_rate', 'unemployment_rate', 'gdp'])
    df['ds'] = pd.to_datetime(df['ds'])
    cursor.close()
    conn.close()
    return df

def run_training_job():
    df = fetch_features()
    df.rename(columns={'cpi': 'y'}, inplace=True)

    df = add_features(df)

    X = df.drop(columns=['ds', 'y'])
    y = df['y']

    model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    model.fit(X, y)
    preds = model.predict(X)

    rmse = root_mean_squared_error(y, preds)
    mape = mean_absolute_percentage_error(y, preds)
    accuracy = 1 - mape

    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
    with mlflow.start_run() as run:
        mlflow.log_param("model_type", "XGBoost")
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("mape", mape)
        mlflow.log_metric("accuracy", accuracy)
        mlflow.set_tag("version", "v1")
        mlflow.sklearn.log_model(model, artifact_path="model")
        print(f"✅ Run logged to MLflow: {run.info.run_id}")
