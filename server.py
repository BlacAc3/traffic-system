from flask import Flask, jsonify, render_template, request, send_from_directory
import os
import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Import existing functions
from traffic_predictor import predict_traffic
from visualizer import visualize_traffic

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/images')
def get_images():
    """Get list of available traffic images"""
    # Only use existing images from the data directory
    image_dir = 'data'
    images = []
    if os.path.exists(image_dir):
        images = [f for f in os.listdir(image_dir)
                  if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    return jsonify({'images': images})

@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    """Analyze a traffic image and return results"""
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
        
    image_path = data.get('image_path')

    if not image_path:
        return jsonify({'error': 'Image path is required'}), 400
        
    if not os.path.exists(image_path):
        return jsonify({'error': f'Image not found: {image_path}'}), 404

    try:
        # Use the existing predict_traffic function
        prediction, counts, img_path = predict_traffic(image_path)

        # Calculate traffic light timings based on analysis
        timings = calculate_traffic_light_timings(counts, prediction)
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

    # Create visualization and convert to base64 for sending to frontend
    try:
        img_buffer = BytesIO()
        plt.figure(figsize=(10, 6))
        visualize_traffic(img_path, counts, prediction)
        plt.savefig(img_buffer, format='png')
        plt.close()
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.read()).decode('utf-8')
    except Exception as e:
        print(f"Visualization error: {e}")
        img_base64 = None

    # Prepare and return response
    response = {
        'prediction': prediction,
        'counts': counts,
        'timings': timings,
        'visualization': img_base64
    }
    
    return jsonify(response)

@app.route('/data/<filename>')
def serve_image(filename):
    """Serve traffic images from the data directory"""
    return send_from_directory('data', filename)

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

if __name__ == '__main__':
    # Make sure required directories exist
    for directory in ['data', 'output']:
        if not os.path.exists(directory):
            os.makedirs(directory)

    app.run(debug=True, port=5000)
