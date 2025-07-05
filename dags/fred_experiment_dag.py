import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from dotenv import load_dotenv
from feature_store.load_features import run as load_features
from feature_store.schema import create_tables

load_dotenv()

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}

with DAG(
    dag_id='fred_experiment_pipeline',
    default_args=default_args,
    schedule='@daily',
    catchup=False,
    tags=['fred', 'ml', 'snowflake'],
) as dag:

    def create_feature_tables():
        create_tables()

    def extract_and_load():
        load_features()

    def train_and_log():
        from ml.train import run_training_job
        run_training_job()

    t1 = PythonOperator(
        task_id='create_feature_store_tables',
        python_callable=create_feature_tables,
    )

    t2 = PythonOperator(
        task_id='load_fred_features_to_snowflake',
        python_callable=extract_and_load,
    )

    t3 = PythonOperator(
        task_id='train_model_and_log_to_mlflow',
        python_callable=train_and_log,
    )

    t1 >> t2 >> t3
