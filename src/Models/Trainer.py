import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import pickle

# Load dataset
data = pd.read_csv('Ad_Fatigue_detector/src/Processed_Data/train_campaign_performance.csv')

# Convert the 'date' column to datetime if necessary
data['date'] = pd.to_datetime(data['date'])

# Drop columns that are unlikely to be useful for prediction
data = data.drop(columns=['campaign_id', 'campaign_name', 'date'])

# Features and target variable
X = data.drop(columns=['fatigue_score'])
y = data['fatigue_score']

# Split the data into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Initialize and train Random Forest Regressor
model = RandomForestRegressor(
    n_estimators=100,
    max_depth=5,
    random_state=42
)
model.fit(X_train_scaled, y_train)

# Save the model to a file
with open('Ad_Fatigue_detector/src/Models/ad_fatigue_model.pkl', 'wb') as f:
    pickle.dump(model, f)
