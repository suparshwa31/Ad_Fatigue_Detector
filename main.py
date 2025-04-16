import os
import pandas as pd
from datetime import datetime
from src.Fatigue.Detector import detect_ad_fatigue
from Analytics.Export_Data import prepare_tableau_data

def run_fatigue_analysis():
    try:

        print("\n1. Running Fatigue Detection...")
        detect_ad_fatigue()
        
        print("\n2. Preparing Data for Tableau...")
        prepare_tableau_data()
        
        print("\n3. Generating Summary Report...")
        generate_summary_report()
        
        print("\nAnalysis Complete! Check the following files:")
        print("- Fatigue Analysis: Ad_Fatigue_detector/src/Fatigue/fatigue_analysis.csv")
        print("- Tableau Data: Ad_Fatigue_detector/Analytics/Data/tableau_fatigue_data_*.csv")
        print("- Summary Report: Ad_Fatigue_detector/Analytics/Reports/fatigue_summary_*.txt")
        
    except Exception as e:
        print(f"\nError in workflow: {e}")

def generate_summary_report():

    try:
        # Load fatigue analysis data
        fatigue_data = pd.read_csv('Ad_Fatigue_detector/src/Fatigue/fatigue_analysis.csv')
        
        # Create reports directory if it doesn't exist
        reports_dir = 'Ad_Fatigue_detector/Analytics/Reports'
        os.makedirs(reports_dir, exist_ok=True)
        
        # Generate timestamp for the filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        # Create summary report
        with open(f'{reports_dir}/fatigue_summary_{timestamp}.txt', 'w') as f:
            f.write("Ad Fatigue Analysis Summary Report\n")
            f.write("===============================\n\n")
            
            # Overall Statistics
            f.write("Overall Statistics:\n")
            f.write("-----------------\n")
            f.write(f"Total Campaigns Analyzed: {len(fatigue_data)}\n")
            f.write(f"Date Range: {fatigue_data['date'].min()} to {fatigue_data['date'].max()}\n\n")
            
            # Fatigue Status Distribution
            f.write("Fatigue Status Distribution:\n")
            f.write("-------------------------\n")
            status_dist = fatigue_data['fatigue_status'].value_counts()
            for status, count in status_dist.items():
                f.write(f"{status}: {count} campaigns ({count/len(fatigue_data)*100:.1f}%)\n")
            f.write("\n")
            
            # Top 5 Most Fatigued Campaigns
            f.write("Top 5 Most Fatigued Campaigns:\n")
            f.write("---------------------------\n")
            top_fatigued = fatigue_data.nsmallest(5, 'predicted_fatigue_score')
            for _, row in top_fatigued.iterrows():
                f.write(f"Campaign: {row['campaign_name']}\n")
                f.write(f"Fatigue Score: {row['predicted_fatigue_score']:.2f}\n")
                f.write(f"Status: {row['fatigue_status']}\n\n")
        
    except Exception as e:
        print(f"Error generating summary report: {e}")

if __name__ == "__main__":
    run_fatigue_analysis() 