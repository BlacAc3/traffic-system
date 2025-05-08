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

#### Generate new traffic data(optional)
Run to generate new sets of traffic images to be analyzed by the model.
```
python main.py
```

### Web Interface

To start the web interface:
```
python server.py
```

Then open your browser and navigate to `http://localhost:5000/`.
