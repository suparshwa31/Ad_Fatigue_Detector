import os
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from datetime import datetime, timedelta
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_google_ads_client():
    """Initialize and return Google Ads API client."""
    credentials = {
        "client_id": os.getenv("GOOGLE_ADS_CLIENT_ID"),
        "client_secret": os.getenv("GOOGLE_ADS_CLIENT_SECRET"),
        "developer_token": os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN"),
        "refresh_token": os.getenv("GOOGLE_ADS_REFRESH_TOKEN"),
        "login_customer_id": os.getenv("GOOGLE_ADS_LOGIN_CUSTOMER_ID"),  # Should be for test account
        "use_proto_plus": True
    }
    return GoogleAdsClient.load_from_dict(credentials)

def fetch_campaign_performance(client, customer_id, date_range_days=30):
    """
    Fetch campaign performance data for the specified date range for a test account.
    """
    ga_service = client.get_service("GoogleAdsService")
    
    # Calculate date range
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=date_range_days)
    
    query = f"""
        SELECT
            campaign.id,
            campaign.name,
            metrics.impressions,
            metrics.clicks,
            metrics.cost_micros,
            metrics.conversions,
            metrics.conversions_value,
            segments.date
        FROM campaign
        WHERE segments.date BETWEEN '{start_date}' AND '{end_date}'
        ORDER BY segments.date DESC
    """
    
    try:
        # Execute the query
        response = ga_service.search(
            customer_id=customer_id,
            query=query
        )
        
        # Process the response
        data = []
        for row in response:
            impressions = row.metrics.impressions
            clicks = row.metrics.clicks
            cost = row.metrics.cost_micros / 1_000_000  # Convert micros to actual currency
            conversions = row.metrics.conversions
            conversion_value = row.metrics.conversions_value

            ctr = (clicks / impressions * 100) if impressions > 0 else 0
            conversion_rate = (conversions / clicks * 100) if clicks > 0 else 0
            cpc = (cost / clicks) if clicks > 0 else 0
            cpa = (cost / conversions) if conversions > 0 else 0
            roas = (conversion_value / cost) if cost > 0 else 0

            data.append({
                'date': row.segments.date,
                'campaign_id': row.campaign.id,
                'campaign_name': row.campaign.name,
                'impressions': impressions,
                'clicks': clicks,
                'cost': cost,
                'conversions': conversions,
                'conversion_value': conversion_value,
                'ctr': ctr,
                'conversion_rate': conversion_rate,
                'cpc': cpc,
                'cpa': cpa,
                'roas': roas
            })
        
        # Convert to DataFrame
        df = pd.DataFrame(data)
        return df
        
    except GoogleAdsException as ex:
        print(f'Request with ID "{ex.request_id}" failed with status '
              f'"{ex.error.code().name}" and includes the following errors:')
        for error in ex.failure.errors:
            print(f'\tError with message "{error.message}".')
            if error.location:
                for field_path_element in error.location.field_path_elements:
                    print(f"\t\tOn field: {field_path_element.field_name}")
        return None

def main():
    """Main function to execute the data fetch."""
    try:
        # Initialize the Google Ads client
        client = get_google_ads_client()
        
        # Get test client account ID from environment variable
        # This should be a different ID than your login_customer_id
        test_client_id = os.getenv("GOOGLE_ADS_TEST_CLIENT_ID")
        
        if not test_client_id:
            print("Error: GOOGLE_ADS_TEST_CLIENT_ID not found in .env file.")
            print("Please add your test client account ID to the .env file.")
            return
        
        # Fetch campaign performance data using the test client account ID
        df = fetch_campaign_performance(client, test_client_id)
        
        if df is not None:
            # Save to CSV
            output_path = "Data/Raw_Data/campaign_performance.csv"
            df.to_csv(output_path, index=False)
            print(f"Data successfully saved to {output_path}")
            
            # Display summary
            print("\nData Summary:")
            print(f"Total records: {len(df)}")
            print(f"Date range: {df['date'].min()} to {df['date'].max()}")
            print(f"Total campaigns: {df['campaign_id'].nunique()}")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
