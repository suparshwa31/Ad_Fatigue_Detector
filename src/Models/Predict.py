import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler

def load_model():
    try:
        with open('Ad_Fatigue_detector/Models/ad_fatigue_model.pkl', 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

def predict_fatigue():
    try:
        test_data = pd.read_csv('Ad_Fatigue_detector/src/Processed_Data/test_campaign_performance.csv')
        
        model = load_model()
        if model is None:
            return
        
        features = test_data.drop(columns=['campaign_id', 'campaign_name', 'date'])
        
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        

        predictions = model.predict(features_scaled)
        
        results = pd.DataFrame({
            'campaign_id': test_data['campaign_id'],
            'campaign_name': test_data['campaign_name'],
            'date': test_data['date'],
            'predicted_fatigue_score': predictions
        })
        
        results = results.sort_values('predicted_fatigue_score')
        
        output_path = 'Ad_Fatigue_detector/src/Models/predicted_fatigue_scores.csv'
        results.to_csv(output_path, index=False)
        
        print(f"\nPredictions saved to: {output_path}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    predict_fatigue() 