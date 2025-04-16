import pandas as pd

def detect_ad_fatigue(input_path='Ad_Fatigue_detector/src/Models/predicted_fatigue_scores.csv', 
                     output_path='Ad_Fatigue_detector/src/Fatigue/fatigue_analysis.csv',
                     threshold=-70):
    try:
        # Load predictions
        df = pd.read_csv(input_path)
        
        # Add fatigue flag based on threshold (more negative = more fatigued)
        df['fatigue_flag'] = df['predicted_fatigue_score'] < threshold
        
        # Add fatigue status label
        df['fatigue_status'] = df['fatigue_flag'].map({
            True: 'FATIGUED',
            False: 'HEALTHY'
        })
        
        # Sort by fatigue score descending
        df = df.sort_values('predicted_fatigue_score', ascending=False)
        
        # Save results
        df.to_csv(output_path, index=False)
        
        print(f"\nResults saved to: {output_path}")
        
    except Exception as e:
        print(f"An error occurred during fatigue detection: {e}")

if __name__ == "__main__":
    detect_ad_fatigue()
