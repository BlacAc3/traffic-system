import cv2
import numpy as np
import os
import pickle

def predict_traffic(image_path=None):
    """
    Predicts traffic density from an image using the trained model.

    Args:
        image_path: Path to the image to analyze. If None, uses the last image in the data directory.

    Returns:
        Prediction result and lane counts
    """
    data_dir = 'data'
    model_path = os.path.join(data_dir, 'traffic_model.pkl')

    # Check if model exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}. Please run model training first.")

    # Load the model
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
    except Exception as e:
        raise Exception(f"Error loading model: {e}")
    
    # Ensure data directory exists
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    # If no image specified, use the last image in data directory
    if image_path is None:
        # Find image files in data directory (support multiple formats)
        image_files = [f for f in os.listdir(data_dir) 
                     if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        if not image_files:
            raise FileNotFoundError("No images found in data directory. Please add images or generate synthetic data first.")

        # Sort by name and get the last one
        image_files.sort()
        image_path = os.path.join(data_dir, image_files[-1])

    # Check if image exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Process the image to extract features
    try:
        img = cv2.imread(image_path)
        if img is None:
            raise Exception(f"Failed to read image: {image_path}")
            
        # Validate image dimensions
        if img.shape[0] == 0 or img.shape[1] == 0:
            raise ValueError(f"Invalid image dimensions: {img.shape}")
    except Exception as e:
        raise Exception(f"Error processing image: {e}")

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
                
            # Get contour area and filter out very small contours (noise)
            area = cv2.contourArea(cnt)
            if area < 100:  # Minimum area threshold
                continue
                
            # Calculate centroid position
            cx = int(M["m10"] / M["m00"])
            
            # Determine which lane the vehicle is in
            lane = min(cx // lane_width, num_lanes - 1)
            counts[lane] += 1
    except Exception as e:
        raise Exception(f"Error in vehicle detection: {e}")

    # Make prediction
    prediction = model.predict([counts])[0]

    return prediction, counts, image_path

if __name__ == "__main__":
    try:
        prediction, counts, image_path = predict_traffic()
        print(f"Analyzed image: {image_path}")
        print(f"Lane counts: {counts}")
        print(f"Traffic prediction: {prediction}")
    except Exception as e:
        print(f"Error: {e}")
