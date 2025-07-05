import os
from datetime import datetime, timedelta
from fredapi import Fred
import pandas as pd
from dotenv import load_dotenv
from ml.utils import get_snowflake_connection

load_dotenv()

def run():
    fred = Fred(api_key=os.getenv("FRED_API_KEY"))

    indicators = {
        "UNRATE": "unemployment_rate",
        "CPIAUCSL": "cpi",            # Consumer Price Index
        "FEDFUNDS": "interest_rate",  # Federal Funds Rate
        "GDPC1": "gdp"                # Real GDP (chained 2012 dollars)
    }

    end_date = datetime.today()
    start_date = end_date - timedelta(days=365 * 10)

    # Fetch and merge all indicators
    data_frames = []
    for code, name in indicators.items():
        df = fred.get_series(code, observation_start=start_date).reset_index()
        df.columns = ['date', name]
        data_frames.append(df)

    df = data_frames[0]
    for other_df in data_frames[1:]:
        df = pd.merge(df, other_df, on='date')

    df['id'] = df['date'].astype(str)
    df['date'] = df['date'].dt.date

    # Reorder columns: id, date, unemployment_rate, cpi, interest_rate, gdp
    ordered_cols = ['id', 'date'] + list(indicators.values())
    df = df[ordered_cols]

    # Upload to Snowflake
    conn = get_snowflake_connection()
    cursor = conn.cursor()

    try:
        for _, row in df.iterrows():
            cursor.execute("""
                MERGE INTO FEATURE_STORE AS target
                USING (SELECT %s AS id, %s AS date, %s AS unemployment_rate, %s AS cpi, %s AS interest_rate, %s AS gdp) AS source
                ON target.id = source.id
                WHEN MATCHED THEN UPDATE SET 
                    unemployment_rate = source.unemployment_rate,
                    cpi = source.cpi,
                    interest_rate = source.interest_rate,
                    gdp = source.gdp
                WHEN NOT MATCHED THEN INSERT (id, date, unemployment_rate, cpi, interest_rate, gdp)
                VALUES (source.id, source.date, source.unemployment_rate, source.cpi, source.interest_rate, source.gdp)
            """, tuple(row))
        print("✅ Features (last 10 years) loaded to Snowflake")
    finally:
        cursor.close()
        conn.close()
