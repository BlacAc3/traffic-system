Using Models to Predict Traffic and Adjust Traffic Lights

Based on the code in this project, I can provide you with a comprehensive overview of how models are used to predict traffic patterns and adjust traffic light timings dynamically.

## Traffic Prediction Models

The system uses a machine learning approach for traffic prediction with these key components:

### 1. Vehicle Detection and Counting
From `traffic_predictor.py`, the system:
- Takes traffic camera images as input
- Converts images to grayscale and applies thresholding
- Uses contour detection to identify vehicles
- Counts vehicles per lane

```traffic-system/traffic_predictor.py#L55-75
# Extract lane counts (similar to feature_extractor)
num_lanes = 4
lane_width = 200

try:
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to create binary image
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Find contours representing vehicles
    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Count vehicles per lane
    counts = [0] * num_lanes
    for cnt in contours:
        # Calculate moments to find centroid
        M = cv2.moments(cnt)
        if M["m00"] == 0:
            continue
```

### 2. Traffic Congestion Classification
From `feature_extractor.py` and `model_trainer.py`:
- The system classifies traffic into three congestion levels: "low", "medium", and "high"
- Features are extracted from images and labeled based on vehicle counts
- A Random Forest classifier is trained on these features

```traffic-system/model_trainer.py#L21-32
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
```

## Traffic Light Adjustment Algorithm

The most important part for your research is in `server.py`, which implements the dynamic traffic light timing algorithm:

```traffic-system/server.py#L79-108
def calculate_traffic_light_timings(counts, prediction):
    """Calculate dynamic traffic light timings based on analysis"""
    total_vehicles = sum(counts) if counts else 0

    # Base timings (in seconds)
    base_green = 30
    base_yellow = 5
    base_red = 40

    # Adjust based on congestion level
    if prediction == "High Congestion":
        congestion_multiplier = 1.5
    elif prediction == "Medium Congestion":
        congestion_multiplier = 1.2
    else:  # Low Congestion
        congestion_multiplier = 1.0

    # Calculate dynamic green light duration
    # More vehicles = longer green light (with an upper limit)
    vehicle_factor = min(2.0, 1.0 + (total_vehicles / 20.0))
    green_duration = int(base_green * congestion_multiplier * vehicle_factor)

    # Cap at reasonable values
    green_duration = min(max(green_duration, 10), 60)

    return {
        'green': green_duration,
        'yellow': base_yellow,
        'red': base_red,
        'vehicle_count': total_vehicles,
        'congestion_level': prediction
    }
```

## How It Works Together

1. **Data Collection**: Traffic camera images are collected or generated
2. **Feature Extraction**: Vehicle counts per lane are extracted from images
3. **Traffic Prediction**: The model classifies traffic congestion as low, medium, or high
4. **Dynamic Timing Calculation**: Traffic light timing is adjusted based on:
   - Total vehicle count (more vehicles = longer green lights)
   - Congestion level (higher congestion = higher multiplier)
   - Base timing values with reasonable minimum/maximum limits

5. **Web Interface Visualization**: The system displays:
   - Traffic congestion predictions
   - Vehicle counts by lane
   - Optimized traffic light timings
   - A simulated traffic light that follows the calculated timings

## Research Implications

This implementation demonstrates several important concepts in traffic management systems:

1. **Computer Vision Integration**: Using image processing to automatically detect vehicles rather than relying on physical sensors
2. **Machine Learning Classification**: Categorizing traffic conditions into discrete levels to inform decision-making
3. **Dynamic Timing Algorithms**: Adjusting traffic light cycles based on real-time data
4. **Multiplier-Based Approaches**: Using base timings modified by congestion factors
5. **Upper/Lower Bounds**: Ensuring timing adjustments remain within reasonable operational parameters

The system follows a model-predict-adjust pattern that could be further enhanced with reinforcement learning algorithms for more adaptive traffic light control.
