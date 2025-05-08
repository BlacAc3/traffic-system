import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

def visualize_traffic(image_path, lane_counts, prediction):
    """
    Visualizes traffic data with lane counts and prediction.

    Args:
        image_path: Path to the traffic image
        lane_counts: List of vehicle counts per lane
        prediction: Traffic density prediction (low, med, high)
    """
    # Check if image exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        raise Exception(f"Failed to read image: {image_path}")

    # Convert BGR to RGB for matplotlib
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Plot the image
    ax1.imshow(img_rgb)
    ax1.set_title('Traffic Image')
    ax1.axis('off')

    # Plot lane counts
    lanes = [f'Lane {i+1}' for i in range(len(lane_counts))]
    ax2.bar(lanes, lane_counts, color='steelblue')
    ax2.set_title(f'Vehicle Counts per Lane (Prediction: {prediction.upper()})')
    ax2.set_ylabel('Number of Vehicles')
    ax2.grid(axis='y', linestyle='--', alpha=0.7)

    # Add total count
    total = sum(lane_counts)
    ax2.text(0.5, 0.9, f'Total: {total} vehicles',
             horizontalalignment='center',
             transform=ax2.transAxes,
             bbox=dict(facecolor='white', alpha=0.8))

    plt.tight_layout()

    # Save visualization
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Extract filename from path
    filename = os.path.basename(image_path)
    base_name = os.path.splitext(filename)[0]
    viz_path = os.path.join(output_dir, f'{base_name}_viz.png')

    plt.savefig(viz_path)
    print(f"Visualization saved to {viz_path}")

    # Display
    plt.show()

def visualize_dataset_summary():
    """
    Creates a summary visualization of the entire dataset
    """
    data_dir = 'data'
    features_path = os.path.join(data_dir, 'features.npz')

    # Check if features exist
    if not os.path.exists(features_path):
        raise FileNotFoundError(f"Features file not found: {features_path}")

    # Load features and labels
    data = np.load(features_path, allow_pickle=True)
    X = data['X']
    y = data['y']


    # Count samples per class
    classes, counts = np.unique(y, return_counts=True)

    # Create a summary visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Class distribution
    ax1.bar(classes, counts, color=['green', 'orange', 'red'])
    ax1.set_title('Class Distribution')
    ax1.set_xlabel('Traffic Density')
    ax1.set_ylabel('Number of Samples')

    # Average vehicles per lane
    avg_per_lane = np.mean(X, axis=0)
    lanes = [f'Lane {i+1}' for i in range(len(avg_per_lane))]
    ax2.bar(lanes, avg_per_lane, color='steelblue')
    ax2.set_title('Average Vehicles per Lane')
    ax2.set_ylabel('Average Count')
    ax2.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()

    # Save visualization
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    viz_path = os.path.join(output_dir, 'dataset_summary.png')
    plt.savefig(viz_path)
    print(f"Dataset summary saved to {viz_path}")

    # Display
    plt.show()

if __name__ == "__main__":
    try:
        # Visualize dataset summary if available
        if os.path.exists(os.path.join('data', 'features.npy')):
            visualize_dataset_summary()
        else:
            print("No dataset features found to visualize")

        # Try to visualize a sample image if available
        data_dir = 'data'
        image_files = [f for f in os.listdir(data_dir) if f.endswith('.png')]

        if image_files:
            # Visualize the first image with some example data
            image_path = os.path.join(data_dir, image_files[0])
            lane_counts = [3, 5, 2, 4]  # Example lane counts
            prediction = "med"  # Example prediction

            visualize_traffic(image_path, lane_counts, prediction)

    except Exception as e:
        print(f"Error in visualization: {e}")
