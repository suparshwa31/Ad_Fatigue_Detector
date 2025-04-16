import pandas as pd
from sklearn.model_selection import train_test_split

def load_raw_data():
    raw_data_path = "Ad_Fatigue_detector/Data/Raw_Data/campaign_performance.csv"
    try:
        df = pd.read_csv(raw_data_path)
        print(f"Successfully loaded {len(df)} records from {raw_data_path}")
        return df
    except FileNotFoundError:
        print(f"Error: {raw_data_path} not found. Please run Raw_Data.py first.")
        return None

def clean_data(df):
    if df is None:
        return None
    
    clean_df = df.copy()
    
    clean_df['date'] = pd.to_datetime(clean_df['date'])
    
    clean_df = clean_df.sort_values(['campaign_id', 'date'])
    
    clean_df = clean_df.drop_duplicates()
    
    numeric_columns = ['impressions', 'clicks', 'cost', 'conversions', 'conversion_value',
                      'ctr', 'conversion_rate', 'cpc', 'cpa', 'roas']
    
    clean_df[numeric_columns] = clean_df[numeric_columns].fillna(0)
    
    clean_df['campaign_name'] = clean_df['campaign_name'].fillna('Unknown Campaign')
    
    
    # Rolling 7-day averages
    for metric in ['impressions', 'clicks', 'ctr', 'conversion_rate']:
        clean_df[f'{metric}_7d_avg'] = clean_df.groupby('campaign_id')[metric].transform(
            lambda x: x.rolling(window=7, min_periods=1).mean()
        )
    
    # Calculate day-over-day changes
    for metric in ['ctr', 'conversion_rate']:
        clean_df[f'{metric}_change'] = clean_df.groupby('campaign_id')[metric].pct_change()
    
    # Calculate fatigue score (based on CTR and conversion rate trends)
    clean_df['fatigue_score'] = (
        (clean_df['ctr_7d_avg'].shift(7) - clean_df['ctr_7d_avg']) / clean_df['ctr_7d_avg'].shift(7) * 100 +
        (clean_df['conversion_rate_7d_avg'].shift(7) - clean_df['conversion_rate_7d_avg']) / clean_df['conversion_rate_7d_avg'].shift(7) * 100
    ) / 2
    

    calculated_fields = ['ctr_change', 'conversion_rate_change', 'fatigue_score']
    clean_df[calculated_fields] = clean_df[calculated_fields].fillna(0)
    
    for metric in numeric_columns:
        mean = clean_df[metric].mean()
        std = clean_df[metric].std()
        clean_df[metric] = clean_df[metric].clip(lower=mean - 3*std, upper=mean + 3*std)
    
    clean_df['campaign_age'] = clean_df.groupby('campaign_id')['date'].transform(
        lambda x: (x - x.min()).dt.days
    )
    
    return clean_df

def save_clean_data(df):
    if df is None:
        return
    

    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    
    test_df = test_df.drop(columns=['fatigue_score'])
    
    train_output_path = "Ad_Fatigue_detector/src/Processed_Data/train_campaign_performance.csv"
    train_df.to_csv(train_output_path, index=False)
    print(f"\nTrain data saved to {train_output_path}")
    
    test_output_path = "Ad_Fatigue_detector/src/Processed_Data/test_campaign_performance.csv"
    test_df.to_csv(test_output_path, index=False)
    print(f"Test data saved to {test_output_path}")
    
    print(f"Total records: {len(df)}")
    print(f"Training records: {len(train_df)}")
    print(f"Test records: {len(test_df)}")

def main():

    try:
        raw_df = load_raw_data()
        
        clean_df = clean_data(raw_df)
        
        save_clean_data(clean_df)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
