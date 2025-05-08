import os
import argparse
from data_generator import generate_traffic_data
from feature_extractor import extract_counts
from model_trainer import train_traffic_model
from traffic_predictor import predict_traffic
from visualizer import visualize_traffic, visualize_dataset_summary

def setup_environment():
    """Ensures required directories exist"""
    dirs = ['data', 'output']
    for directory in dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")

def main():
    """Main function to run the traffic system"""
    parser = argparse.ArgumentParser(description='Traffic Analysis System')
    parser.add_argument('--generate', action='store_true', help='Generate synthetic traffic data')
    parser.add_argument('--extract', action='store_true', help='Extract features from images')
    parser.add_argument('--train', action='store_true', help='Train the traffic model')
    parser.add_argument('--predict', type=str, nargs='?', const=None, help='Path to image for prediction')
    parser.add_argument('--visualize', action='store_true', help='Visualize results')
    parser.add_argument('--summary', action='store_true', help='Generate dataset summary')
    parser.add_argument('--all', action='store_true', help='Run the entire pipeline')

    args = parser.parse_args()

    # Ensure directories exist
    setup_environment()

    # Run all steps if --all is specified or no specific step is requested
    run_all = args.all or not any([args.generate, args.extract, args.train,
                                  args.predict is not None, args.visualize, args.summary])

    # Generate data
    if args.generate or run_all:
        print("\n--- Generating Traffic Data ---")
        generate_traffic_data(num_samples=5)

    # Extract features
    if args.extract or run_all:
        print("\n--- Extracting Features ---")
        extract_counts()

    # # Train model
    # if args.train or run_all:
    #     print("\n--- Training Model ---")
    #     train_traffic_model()

    # Make predictions
    prediction = None
    counts = None
    image_path = None

    if args.predict is not None or run_all:
        print("\n--- Making Predictions ---")
        prediction, counts, image_path = predict_traffic(args.predict)
        print(f"Analyzed image: {image_path}")
        print(f"Lane counts: {counts}")
        print(f"Traffic prediction: {prediction}")

    # Visualize the prediction
    if (args.visualize or run_all) and prediction is not None:
        print("\n--- Visualizing Results ---")
        visualize_traffic(image_path, counts, prediction)

    # Generate dataset summary
    if args.summary or run_all:
        print("\n--- Generating Dataset Summary ---")
        try:
            visualize_dataset_summary()
        except FileNotFoundError:
            print("Dataset features not found. Run extraction first.")

    print("\nDone!")

if __name__ == "__main__":
    main()
