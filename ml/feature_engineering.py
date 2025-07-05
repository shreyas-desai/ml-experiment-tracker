def add_features(df):
    for lag in [1, 3, 6]:
        for col in ['y', 'interest_rate', 'unemployment_rate', 'gdp']:
            df[f"{col}_lag_{lag}"] = df[col].shift(lag)
    df['month'] = df['ds'].dt.month
    df['quarter'] = df['ds'].dt.quarter
    return df.dropna()