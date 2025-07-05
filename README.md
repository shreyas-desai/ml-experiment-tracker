# 📈 ML Experiment Tracker: Forecasting Economic Indicators

This project is a complete machine learning pipeline for forecasting U.S. macroeconomic indicators, specifically the ***Consumer Price Index (CPI)***, using data from the ***Federal Reserve Economic Data (FRED)***. It integrates data ingestion, feature engineering, model training (*XGBoost*), experiment tracking with *MLflow*, and visualization with *Streamlit*. The entire workflow is orchestrated via **Apache Airflow** and persisted in **Snowflake**.

---

## 📦 Project Structure
```bash
├── dags/                        # Airflow DAGs for automation
│   └── fred_experiment_dag.py
├── feature_store/              # FRED data ingestion and schema setup
│   ├── load_features.py
│   └── schema.py
├── ml/                         # Model training and utilities
│   ├── train.py
│   ├── feature_engineering.py
│   └── utils.py
├── streamlit_app/              # CPI forecast visualization
│   └── app.py
├── docker-compose.yaml         # Docker orchestration for Airflow, MLflow, Streamlit
├── dockerfile                  # Dockerfile for ML services
├── .env                        # Environment variables (Snowflake, MLflow, FRED API keys)
└── requirements.txt            # Python dependencies
```

## 🚀 Features
- Data Pipeline: Automatically fetches 10 years of economic indicators (CPI, GDP, Interest Rate, Unemployment Rate) from FRED API and stores it in Snowflake.

- Feature Engineering: Adds lag features and time-based signals (month, quarter).

- Training & Tracking: Trains an XGBoost regression model, logs performance metrics (RMSE, MAPE, Accuracy) and model artifacts to MLflow.

- Web App: Streamlit dashboard to compare actual vs predicted CPI.

- Automation: Apache Airflow DAG automates the creation of tables, data ingestion, and model training.
## ⚙️ Setup & Run

### 1. Clone the Repo

```bash
git clone https://github.com/shreyas-desai/ml-experiment-tracker.git
cd ml-experiment-tracker
```

### 2. Configure Environment Variables
Create a ```.env``` file in the root:

```env
# FRED API
FRED_API_KEY=your_fred_api_key

# Snowflake
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_user
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_DATABASE=FRED_ML_PROJECT
SNOWFLAKE_SCHEMA=EXPERIMENTS
SNOWFLAKE_WAREHOUSE=COMPUTE_WH

# MLflow
MLFLOW_TRACKING_URI=http://mlflow:5000
MLFLOW_EXPERIMENT_NAME=FRED_ML_PROJECT
```

### 3. Run the Project (via Docker Compose)
```bash
docker compose up --build
```

This launches:

- Apache Airflow (ETL + training scheduling)

- MLflow tracking server: http://localhost:5000

- Streamlit frontend: http://localhost:8501

## 🧪 ML Model Training
Model training is triggered by the Airflow DAG fred_experiment_pipeline, but you can run it manually:

```bash
docker compose exec airflow-worker python feature_store/schema.py
docker compose exec airflow-worker python ml/train.py
```

## 📊 Streamlit Dashboard
Once training is complete and a model is registered, go to:
```bash
http://localhost:8501
```

Dashboard Sections:

- 📈 Actual vs Predicted CPI Forecast

- 📋 Latest Dataframe

- ✅ Model Version Info
## 📈 DAG Tasks Breakdown

| Task                           | Description                                      |
|--------------------------------|--------------------------------------------------|
| `create_feature_store_tables`     | Creates Snowflake tables if they don’t exist     |
| `load_fred_features_to_snowflake` | Loads 10 years of FRED data to Snowflake     |
| `train_model_and_log_to_mlflow`   | Trains XGBoost model and logs it to MLflow     |

## 📦 Tech Stack
- Apache Airflow: DAG orchestration
- FRED API: Economic data ingestion
- Snowflake: Feature storage
- XGBoost: Forecast model
- MLflow: Experiment tracking
- Streamlit: Visualization
- Docker & Docker Compose: Environment setup



## 🙌 Contributing

Feel free to fork this repository and submit pull requests if you have ideas to improve the pipeline, add new economic indicators, or experiment with alternative models.



## 📬 Questions or Feedback?

If you have any questions, suggestions, or feedback, feel free to open an issue or reach out to me `shreyasdesai3013@gmail.com`. Contributions are always welcome to make this project more robust and insightful.



**Thanks for checking out this project! Happy forecasting 📊**
