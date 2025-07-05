import os
import mlflow
import pandas as pd
import streamlit as st
import joblib
from dotenv import load_dotenv
from ml.feature_engineering import add_features
from ml.utils import get_snowflake_connection
from mlflow.pyfunc import load_model
load_dotenv()

st.title("📈 CPI Forecast Visualizer")

mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))

client = mlflow.tracking.MlflowClient()
experiment = client.get_experiment_by_name("FRED_ML_PROJECT")
runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["start_time desc"]
)
latest_run = runs[0]
# model_uri = f"{latest_run.info.artifact_uri}/model.pkl"

try:
    model = load_model(f"runs:/{latest_run.info.run_id}/model")
    # model = load_model(f"file:/{latest_run.info.run_id}/artifacts/model.pkl")
    # st.success(f"Loaded model: {model_uri}")
    st.success(f"Loaded model from run ID: {latest_run.info.run_id}")
except Exception as e:
    st.error(f"Failed to load model: {e}")
    st.error(latest_run)
    st.stop()

# Load input features from Snowflake
# @st.cache_data
def get_latest_data():
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    query = """
        SELECT date, cpi, interest_rate, unemployment_rate, gdp
        FROM FEATURE_STORE
        ORDER BY date
    """
    cursor.execute(query)
    df = pd.DataFrame(cursor.fetchall(), columns=['ds', 'y', 'interest_rate', 'unemployment_rate', 'gdp'])
    df['ds'] = pd.to_datetime(df['ds'])
    cursor.close()
    conn.close()
    return df

df = get_latest_data()
df = add_features(df)

X = df.drop(columns=['ds', 'y'])
y = df['y']
preds = model.predict(X)

# Plot actual vs predicted
st.subheader("🔍 Actual vs Predicted CPI")
plot_df = pd.DataFrame({'ds': df['ds'], 'actual': y, 'predicted': preds})
st.line_chart(plot_df.set_index('ds'))

with st.expander("📋 Raw Forecast Data"):
    st.dataframe(plot_df.tail(12))
