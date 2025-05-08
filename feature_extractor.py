import cv2
import numpy as np
import os

def extract_counts():
    """
    Reads each synthetic frame, thresholds to binary,
    finds contour centroids, and counts per lane.
    Labels total traffic as 'low', 'med', or 'high'.
    """
    # Must match simulator settings
    num_lanes = 4
    lane_width = 200
    input_dir = 'data'
    output_file = os.path.join(input_dir, 'features.npz')

    # Check if data directory exists
    if not os.path.exists(input_dir):
        raise FileNotFoundError(f"Data directory not found: {input_dir}")

    metadata_path = os.path.join(input_dir, 'metadata.npy')
    if not os.path.exists(metadata_path):
        raise FileNotFoundError(f"Metadata file not found: {metadata_path}")

    # Load frame metadata
    try:
        metadata = np.load(metadata_path, allow_pickle=True)
    except Exception as e:
        raise Exception(f"Error loading metadata: {e}")

    X, y = [], []
    for fname, true_counts in metadata:
        img_path = os.path.join(input_dir, fname)
        if not os.path.exists(img_path):
            print(f"Warning: Image not found: {img_path}")
            continue

        img = cv2.imread(img_path)
        if img is None:
            print(f"Warning: Failed to read image: {img_path}")
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        # Count vehicles per lane
        counts = [0] * num_lanes
        for cnt in contours:
            M = cv2.moments(cnt)
            if M["m00"] == 0:
                continue
            cx = int(M["m10"] / M["m00"])
            lane = min(cx // lane_width, num_lanes - 1)
            counts[lane] += 1

        X.append(counts)
        total = sum(true_counts)
        if total <= 10:
            y.append("low")
        elif total <= 20:
            y.append("med")
        else:
            y.append("high")

    X_array = np.array(X, dtype=object)
    y_array = np.array(y, dtype=object)

    if not X:
        print("Warning: No features extracted!")
        return

    try:
        np.savez( output_file, X = X_array, y = y_array)
        print(f"Extracted {len(X)} samples to '{output_file}'")
    except Exception as e:
        print(f"Error saving features: {e}")

if __name__ == '__main__':
    try:
        extract_counts()
    except Exception as e:
        print(f"Error: {e}")
