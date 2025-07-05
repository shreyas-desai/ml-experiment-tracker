import os
import snowflake.connector
import sys
import os

from dotenv import load_dotenv
load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ml.utils import get_snowflake_connection



def create_tables():
    conn = get_snowflake_connection()
    cs = conn.cursor()

    try:
        cs.execute("""
            CREATE TABLE IF NOT EXISTS FEATURE_STORE (
                id STRING,
                date DATE,
                unemployment_rate FLOAT,
                cpi FLOAT,
                interest_rate FLOAT,
                gdp FLOAT
            )
        """)
        cs.execute("""
            CREATE TABLE IF NOT EXISTS MODEL_RESULTS (
                run_id STRING,
                model_version STRING,
                metric_rmse FLOAT,
                training_date TIMESTAMP,
                parameters VARIANT
            )
        """)
        print("✅ Tables created or already exist.")
    finally:
        cs.close()
        conn.close()

if __name__ == "__main__":
    create_tables()
