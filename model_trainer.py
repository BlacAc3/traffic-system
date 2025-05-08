import numpy as np
import os
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

def train_traffic_model():
    """
    Trains a model to classify traffic density based on lane counts.
    """
    data_dir = 'data'
    features_path = os.path.join(data_dir, 'features.npz')
    model_path = os.path.join(data_dir, 'traffic_model.pkl')

    # Check if features file exists
    if not os.path.exists(features_path):
        raise FileNotFoundError(f"Features file not found: {features_path}")

    try:
        # Load features and labels
        data = np.load(features_path, allow_pickle=True)
        X = data['X']
        y = data['y']

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Initialize and train the model
        model = RandomForestClassifier(n_estimators=100, random_state=42 )
        model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Model accuracy: {accuracy:.4f}")
        print(classification_report(y_test, y_pred))

        # Save the model
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        print(f"Model saved to '{model_path}'")

        return model

    except Exception as e:
        print(f"Error in model training: {e}")
        return None

if __name__ == "__main__":
    try:
        train_traffic_model()
    except Exception as e:
        print(f"Error: {e}")
