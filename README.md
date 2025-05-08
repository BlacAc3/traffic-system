# Traffic Analysis System

## Overview

The Traffic Analysis System is a comprehensive tool for analyzing traffic flow and congestion levels from traffic camera images. The system can generate synthetic traffic data, extract vehicle counts from images, predict congestion levels, and calculate optimal traffic light timings based on the analysis.

Key features:
- Generation of synthetic traffic data for testing
- Vehicle detection and counting in traffic images
- Traffic congestion prediction (Low, Medium, High)
- Dynamic traffic light timing calculations
- Visualization of analysis results
- Web interface for easy interaction

## Installation

### 1. Install Python

**For Windows:**
1. Download the latest Python installer from [python.org](https://www.python.org/downloads/)
2. Run the installer and check "Add Python to PATH" during installation
3. Verify installation by opening a command prompt and typing: `python --version`

**For Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip

# Verify installation
python3 --version
```

### 2. Clone the repository:
```bash
git clone https://github.com/blacac3/traffic-system.git
cd traffic-system
```

### 3. Set up a virtual environment:

**For Windows:**
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
venv\Scripts\activate
```

**For Linux:**
```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### 4. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

The system can be operated through the `main.py` file, which provides several options:

#### Generate new traffic data
```
python main.py
```

### Web Interface

To start the web interface:
```
python server.py
```

Then open your browser and navigate to `http://localhost:5000/`.

## Project Structure

- `/data`: Contains traffic images (both synthetic and real)
- `/output`: Contains analysis results and visualizations
- `/templates`: HTML templates for the web interface
- `/static`: Static files for the web interface (CSS, JavaScript)

## Workflow

1. Generate traffic data or add your own traffic images to the `/data` directory
2. Extract vehicle counts from the images
3. Train the model on the extracted features
4. Make predictions on new images
5. Visualize the results
6. Optionally use the web interface for a more user-friendly experience
