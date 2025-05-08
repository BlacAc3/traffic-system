import cv2
import numpy as np
import os
import random

def generate_traffic_data(num_samples=100, num_lanes=4, lane_width=200, height=600):
    """
    Generates synthetic traffic data and saves images and metadata.
    """
    # Create data directory if it doesn't exist
    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created directory: {data_dir}")

    # Set up image dimensions
    width = num_lanes * lane_width

    metadata = []

    for i in range(num_samples):
        # Create a blank image (road)
        img = np.zeros((height, width, 3), dtype=np.uint8)
        img[:, :] = (50, 50, 50)  # Dark gray background for road

        # Draw lane markings
        for lane in range(1, num_lanes):
            x = lane * lane_width
            cv2.line(img, (x, 0), (x, height), (255, 255, 255), 2)

        # Generate random number of vehicles per lane
        true_counts = []
        for lane in range(num_lanes):
            # Random number of vehicles in this lane (0-10)
            num_vehicles = random.randint(0, 10)
            true_counts.append(num_vehicles)

            # Create vehicles in this lane
            for _ in range(num_vehicles):
                # Vehicle size
                w, h = random.randint(40, 60), random.randint(80, 120)

                # Vehicle position
                x = lane * lane_width + random.randint(20, lane_width - w - 20)
                y = random.randint(0, height - h)

                # Vehicle color (random bright color)
                color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))

                # Draw vehicle
                cv2.rectangle(img, (x, y), (x + w, y + h), color, -1)

        # Save the image
        filename = f"traffic_{i:04d}.png"
        file_path = os.path.join(data_dir, filename)
        cv2.imwrite(file_path, img)

        # Add to metadata
        metadata.append((filename, true_counts))

    metadata_array = np.array(metadata, dtype=object)  # 📌 key change


    # Save metadata - FIX: added allow_pickle=True
    np.save(os.path.join(data_dir, 'metadata.npy'), metadata_array, allow_pickle=True)
    print(f"Generated {num_samples} traffic images and saved metadata")

if __name__ == "__main__":
    try:
        generate_traffic_data()
    except Exception as e:
        print(f"Error in data generation: {e}")
