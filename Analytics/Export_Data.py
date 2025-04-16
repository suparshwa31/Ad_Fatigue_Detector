import pandas as pd
import os
from datetime import datetime

def prepare_tableau_data():
    """
    Prepare and export data for Tableau visualization.
    Creates a comprehensive dataset with all necessary metrics for visualization.
    """
    try:
        # Load the fatigue analysis data
        tableau_data = pd.read_csv('Ad_Fatigue_detector/src/Fatigue/fatigue_analysis.csv')
        
        # Convert date column to datetime
        tableau_data['date'] = pd.to_datetime(tableau_data['date'])
        
        # Add time-based columns for Tableau
        tableau_data['year'] = tableau_data['date'].dt.year
        tableau_data['month'] = tableau_data['date'].dt.month
        tableau_data['day'] = tableau_data['date'].dt.day
        tableau_data['day_of_week'] = tableau_data['date'].dt.day_name()
        
        # Calculate additional metrics for visualization
        tableau_data['fatigue_severity'] = pd.cut(
            tableau_data['predicted_fatigue_score'],
            bins=[-float('inf'), -100, -50, -25, 0, float('inf')],
            labels=['Critical', 'High', 'Medium', 'Low', 'Healthy']
        )
        
        # Select and order columns for Tableau
        columns_for_tableau = [
            'date', 'year', 'month', 'day', 'day_of_week',
            'campaign_id', 'campaign_name',
            'predicted_fatigue_score', 'fatigue_flag', 'fatigue_status',
            'fatigue_severity'
        ]
        
        tableau_data = tableau_data[columns_for_tableau]
        
        # Create output directory if it doesn't exist
        output_dir = 'Ad_Fatigue_detector/Analytics/Data'
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate timestamp for the filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Save to CSV
        output_path = f'{output_dir}/tableau_fatigue_data_{timestamp}.csv'
        tableau_data.to_csv(output_path, index=False)
        
        # Print summary
        print("\nTableau Data Export Summary:")
        print("===========================")
        print(f"Total records: {len(tableau_data)}")
        print(f"Date range: {tableau_data['date'].min()} to {tableau_data['date'].max()}")
        print(f"Total campaigns: {tableau_data['campaign_id'].nunique()}")
        print(f"\nFatigue Status Distribution:")
        print(tableau_data['fatigue_status'].value_counts())
        print(f"\nFatigue Severity Distribution:")
        print(tableau_data['fatigue_severity'].value_counts())
        print(f"\nData exported to: {output_path}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    prepare_tableau_data() 