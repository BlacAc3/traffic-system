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

    try:
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
        ax1.set_title('Traffic Image', fontsize=12, fontweight='bold')
        ax1.axis('off')

        # Create color map based on congestion level
        if prediction.lower() == 'high':
            bar_color = '#e74c3c'  # Red for high congestion
            title_color = '#c0392b'
        elif prediction.lower() == 'med':
            bar_color = '#f39c12'  # Orange for medium congestion
            title_color = '#d35400'
        else:  # low
            bar_color = '#2ecc71'  # Green for low congestion
            title_color = '#27ae60'

        # Plot lane counts with styled bars
        lanes = [f'Lane {i+1}' for i in range(len(lane_counts))]
        bars = ax2.bar(lanes, lane_counts, color=bar_color, alpha=0.8, 
                      edgecolor='black', linewidth=1)
        
        # Add data labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
                    
        # Style the bar chart
        ax2.set_title(f'Vehicle Counts by Lane\n(Prediction: {prediction.upper()})', 
                     fontsize=12, fontweight='bold', color=title_color)
        ax2.set_ylabel('Number of Vehicles', fontweight='bold')
        ax2.set_ylim(0, max(lane_counts) * 1.2 + 1)  # Add some space for labels
        ax2.grid(axis='y', linestyle='--', alpha=0.7)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)

        # Add total count with styled text box
        total = sum(lane_counts)
        ax2.text(0.5, 0.9, f'Total: {total} vehicles',
                horizontalalignment='center',
                transform=ax2.transAxes,
                bbox=dict(facecolor='white', alpha=0.9, boxstyle='round,pad=0.5',
                          edgecolor=bar_color))
    except Exception as e:
        # If visualization fails, create a simple error figure
        plt.figure(figsize=(8, 6))
        plt.text(0.5, 0.5, f"Visualization Error: {str(e)}", 
                 ha='center', va='center', fontsize=12)
        plt.axis('off')
        print(f"Error in visualization: {e}")

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
        raise FileNotFoundError(f"Features file not found: {features_path}. Run feature extraction first.")

    try:
        # Load features and labels
        data = np.load(features_path, allow_pickle=True)
        X = data['X']
        y = data['y']

        # Count samples per class
        classes, counts = np.unique(y, return_counts=True)

        # Map class names to readable format
        class_names = []
        colors = []
        for cls in classes:
            if cls == 'low':
                class_names.append('Low Congestion')
                colors.append('#2ecc71')  # Green
            elif cls == 'med':
                class_names.append('Medium Congestion')
                colors.append('#f39c12')  # Orange
            else:  # high
                class_names.append('High Congestion')
                colors.append('#e74c3c')  # Red

        # Create a summary visualization with better styling
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Class distribution with better styling
        bars = ax1.bar(class_names, counts, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
        
        # Add data labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{int(height)}', ha='center', va='bottom', fontweight='bold')
                    
        ax1.set_title('Traffic Congestion Distribution', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Congestion Level', fontweight='bold')
        ax1.set_ylabel('Number of Samples', fontweight='bold')
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.grid(axis='y', linestyle='--', alpha=0.3)

        # Average vehicles per lane with better styling
        avg_per_lane = np.mean(X, axis=0)
        lanes = [f'Lane {i+1}' for i in range(len(avg_per_lane))]
        bars = ax2.bar(lanes, avg_per_lane, color='#3498db', alpha=0.8, edgecolor='black', linewidth=1)
        
        # Add data labels on top of bars
        for bar in bars:
            height = bar.get_height()
            ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height:.1f}', ha='center', va='bottom', fontweight='bold')
                    
        ax2.set_title('Average Vehicles per Lane', fontsize=12, fontweight='bold')
        ax2.set_ylabel('Average Count', fontweight='bold')
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)
        ax2.grid(axis='y', linestyle='--', alpha=0.3)
        
        # Add overall stats as text
        total_samples = len(X)
        avg_total_vehicles = np.mean([sum(x) for x in X])
        ax1.text(0.5, -0.2, 
                f'Dataset Summary: {total_samples} samples with {avg_total_vehicles:.1f} vehicles per image on average',
                ha='center', transform=ax1.transAxes, fontsize=11, fontweight='bold',
                bbox=dict(facecolor='#f8f9fa', alpha=0.9, boxstyle='round,pad=0.5', edgecolor='#bdc3c7'))
    except Exception as e:
        # Create error figure if visualization fails
        plt.figure(figsize=(10, 6))
        plt.text(0.5, 0.5, f"Dataset Summary Error: {str(e)}", 
                ha='center', va='center', fontsize=12)
        plt.axis('off')
        print(f"Error in dataset visualization: {e}")

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
