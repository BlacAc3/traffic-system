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
        timings = calculate_traffic_light_timings_per_lane(counts, prediction)
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

def calculate_traffic_light_timings_per_lane(counts, prediction):
    """
    Calculate dynamic traffic light timings for each of four lanes.

    Args:
        counts (list of int): vehicle counts for lanes 1–4, e.g. [c1, c2, c3, c4].
        prediction (str): one of "High Congestion", "Medium Congestion", or "Low Congestion".

    Returns:
        dict: {
            0: {'green': G1, 'yellow': Y, 'red': R1},
            1: {'green': G2, 'yellow': Y, 'red': R2},
            2: {'green': G3, 'yellow': Y, 'red': R3},
            3: {'green': G4, 'yellow': Y, 'red': R4},
            'cycle_length': C
        }
    """
    # Ensure we have exactly 4 lanes
    if not counts or len(counts) != 4:
        raise ValueError("counts must be a list of 4 non-negative integers")

    total_vehicles = sum(counts)
    # Base cycle parameters
    base_green = 30     # nominal total green-time budget (sec) to split among lanes
    base_yellow = 5     # fixed per-lane yellow
    base_red = 40       # nominal red (will be adjusted per lane)
    min_green = 10      # per-lane minimum green
    max_green = 60      # per-lane maximum green

    # Congestion multiplier
    if prediction == "High Congestion":
        cong_mul = 1.5
    elif prediction == "Medium Congestion":
        cong_mul = 1.2
    else:  # Low Congestion
        cong_mul = 1.0

    # Adjust the total green budget by congestion
    green_budget = int(base_green * cong_mul)
    # Distribute green_budget proportionally, or equally if no vehicles
    if int(total_vehicles) > 0:
        ratios = [c / total_vehicles for c in counts]
    else:
        ratios = [0.25] * 4  # equal share if no vehicles

    # Build per-lane timings
    timings = {}
    cycle_length = 0
    for lane_idx, ratio in enumerate(ratios):
        g = int(green_budget * ratio)
        # enforce per-lane clamps
        g = max(min_green, min(g, max_green))
        y = base_yellow
        # red is cycle minus (green + yellow)
        # here assume cycle is green_budget + yellow + base_red
        # so each lane’s red = (green_budget + base_red) - (g + y)
        lane_cycle = green_budget + base_red
        r = lane_cycle - (g + y)
        timings[str(lane_idx)] = {'green': g, 'yellow': y, 'red': r}
        cycle_length = max(cycle_length, lane_cycle)

    timings['cycle_length'] = cycle_length
    return timings

if __name__ == '__main__':
    # Make sure required directories exist
    for directory in ['data', 'output']:
        if not os.path.exists(directory):
            os.makedirs(directory)

    app.run(debug=True, port=5000)
