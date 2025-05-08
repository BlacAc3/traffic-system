document.addEventListener("DOMContentLoaded", function () {
  // Load available images
  fetchImages();
});

let trafficLightInterval = null;

async function fetchImages() {
  try {
    const response = await fetch("/api/images");
    const data = await response.json();

    if (data.images && data.images.length > 0) {
      displayImages(data.images);
    } else {
      document.getElementById("image-grid").innerHTML =
        "<p>No traffic images available</p>";
    }
  } catch (error) {
    console.error("Error fetching images:", error);
    document.getElementById("image-grid").innerHTML =
      "<p>Error loading images. Please try again.</p>";
  }
}

function displayImages(images) {
  const grid = document.getElementById("image-grid");
  grid.innerHTML = "";

  images.forEach((imageName) => {
    const imagePath = `data/${imageName}`;

    const imageItem = document.createElement("div");
    imageItem.className = "image-item";
    imageItem.addEventListener("click", () => selectImage(imagePath));

    const img = document.createElement("img");
    img.src = `/data/${imageName}`;
    img.alt = `Traffic Image: ${imageName}`;

    imageItem.appendChild(img);
    grid.appendChild(imageItem);
  });
}

async function selectImage(imagePath, event) {
  // Highlight selected image with smooth transition
  document.querySelectorAll(".image-item").forEach((item) => {
    item.classList.remove("selected");
  });

  // Get the clicked element and add selected class
  const selectedItem = event
    ? event.currentTarget
    : document.querySelector(`[data-path="${imagePath}"]`);
  if (selectedItem) {
    selectedItem.classList.add("selected");
    // Scroll the image into view if needed
    selectedItem.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  // Create an enhanced loading indicator with subtle colors and animation
  const resultsContainer = document.getElementById("analysis-results");
  resultsContainer.innerHTML = `
    <div class="analysis-loading">
      <div class="loading-spinner-container">
        <div class="loading-spinner"></div>
        <div class="loading-spinner-overlay"></div>
      </div>
      <h4 class="loading-title">Analyzing Traffic Image</h4>
      <div class="loading-progress">
        <div class="progress-bar">
          <div class="progress-fill"></div>
        </div>
        <p class="loading-step active-step">Detecting vehicles...</p>
        <p class="loading-step">Analyzing congestion patterns</p>
        <p class="loading-step">Calculating optimal timing</p>
      </div>
    </div>
  `;

  // Animate progress steps
  const progressFill = resultsContainer.querySelector(".progress-fill");
  const loadingSteps = resultsContainer.querySelectorAll(".loading-step");
  progressFill.style.width = "10%";

  // Start progress animation
  setTimeout(() => {
    progressFill.style.transition = "width 1.5s ease-in-out";
    progressFill.style.width = "40%";
    loadingSteps[0].classList.remove("active-step");
    loadingSteps[1].classList.add("active-step");
  }, 800);

  // Clear previous visualization with pulsing placeholder
  document.getElementById("visualization").innerHTML = `
    <div class="visualization-placeholder">
      <div class="pulse-container">
        <div class="pulse-ring"></div>
        <div class="pulse-circle"></div>
      </div>
      <p>Generating visualization<span class="loading-dots"><span>.</span><span>.</span><span>.</span></span></p>
    </div>
  `;

  // Animate loading dots
  const loadingDots = document.querySelectorAll(".loading-dots span");
  let dotIndex = 0;
  const dotAnimation = setInterval(() => {
    loadingDots.forEach((dot) => dot.classList.remove("active"));
    loadingDots[dotIndex].classList.add("active");
    dotIndex = (dotIndex + 1) % loadingDots.length;
  }, 400);

  try {
    // Show the image being analyzed with a subtle highlight
    const previewContainer = document.createElement("div");
    previewContainer.className = "analysis-preview";
    previewContainer.innerHTML = `
      <div class="preview-image-container">
        <div class="scanning-line"></div>
        <img src="${imagePath.replace("data/", "/data/")}" alt="Analyzing this image">
      </div>
    `;
    resultsContainer.appendChild(previewContainer);

    // Update progress
    setTimeout(() => {
      progressFill.style.width = "70%";
      loadingSteps[1].classList.remove("active-step");
      loadingSteps[2].classList.add("active-step");
    }, 1800);

    // Make API request
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ image_path: imagePath }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(
        errorData.message || `Analysis failed (${response.status})`,
      );
    }

    const data = await response.json();

    // Complete the progress animation
    progressFill.style.width = "100%";
    progressFill.style.backgroundColor = "#4CAF50";

    // Clear interval for dots animation
    clearInterval(dotAnimation);

    // Add a subtle fade-in effect for results with color transition
    resultsContainer.style.opacity = "0";
    displayAnalysisResults(data);
    setTimeout(() => {
      resultsContainer.style.transition =
        "opacity 0.8s ease, transform 0.5s ease";
      resultsContainer.style.transform = "translateY(0)";
      resultsContainer.style.opacity = "1";
    }, 300);

    // Start traffic light simulation with visual feedback
    const timingDisplay = document.getElementById("timing-display");
    timingDisplay.innerHTML = `
      <div class="timing-calculation">
        <div class="timing-indicator"></div>
        <p>Calculating optimal traffic light timing...</p>
      </div>
    `;
    setTimeout(() => startTrafficLightSimulation(data.timings), 500);
  } catch (error) {
    console.error("Error:", error);

    // Clear interval for dots animation
    clearInterval(dotAnimation);

    document.getElementById("analysis-results").innerHTML = `
      <div class="analysis-error">
        <div class="error-icon">
          <svg viewBox="0 0 24 24" width="32" height="32">
            <circle cx="12" cy="12" r="11" fill="#ffebee" />
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z" fill="#f44336"/>
          </svg>
        </div>
        <h4>Analysis Error</h4>
        <p>${error.message || "Failed to analyze the image. Please try again."}</p>
        <button class="retry-button" onclick="selectImage('${imagePath}')">
          <span class="retry-icon">↻</span> Try Again
        </button>
      </div>
    `;
  }
}

function displayAnalysisResults(data) {
  const resultsContainer = document.getElementById("analysis-results");

  // Determine congestion class for styling
  let congestionClass = "congestion-low";
  if (data.prediction.includes("High")) {
    congestionClass = "congestion-high";
  } else if (data.prediction.includes("Medium")) {
    congestionClass = "congestion-medium";
  }

  // Build results HTML
  let html = `
        <h3>Analysis Results</h3>
        <p>Prediction: <span class="${congestionClass}">${data.prediction}</span></p>
        <h4>Vehicle Counts:</h4>
        <ul>
    `;

  // Add vehicle counts for each lane
  for (const [lane, count] of Object.entries(data.counts)) {
    html += `<li>${lane}: ${count} vehicles</li>`;
  }

  html += `</ul>
        <h4>Traffic Light Timing:</h4>
        <ul>
            <li>Green: ${data.timings.green} seconds</li>
            <li>Yellow: ${data.timings.yellow} seconds</li>
            <li>Red: ${data.timings.red} seconds</li>
        </ul>
        <p>Total vehicles: ${data.timings.vehicle_count}</p>
    `;

  resultsContainer.innerHTML = html;

  // Display visualization
  if (data.visualization) {
    const visualizationContainer = document.getElementById("visualization");
    visualizationContainer.innerHTML = `
            <img src="data:image/png;base64,${data.visualization}"
                 alt="Traffic Analysis Visualization">
        `;
  }
}

function startTrafficLightSimulation(timings) {
  // Clear any existing simulation
  if (trafficLightInterval) {
    clearInterval(trafficLightInterval);
  }

  const redLight = document.getElementById("red-light");
  const yellowLight = document.getElementById("yellow-light");
  const greenLight = document.getElementById("green-light");
  const timingDisplay = document.getElementById("timing-display");

  // Reset all lights
  redLight.classList.remove("active");
  yellowLight.classList.remove("active");
  greenLight.classList.remove("active");

  // Start with green
  let currentLight = "green";
  let timeRemaining = timings.green;
  greenLight.classList.add("active");

  updateTimingDisplay(currentLight, timeRemaining);

  // Run the traffic light cycle
  trafficLightInterval = setInterval(() => {
    timeRemaining--;

    updateTimingDisplay(currentLight, timeRemaining);

    if (timeRemaining <= 0) {
      // Switch to next light
      switch (currentLight) {
        case "green":
          // Green → Yellow
          greenLight.classList.remove("active");
          yellowLight.classList.add("active");
          currentLight = "yellow";
          timeRemaining = timings.yellow;
          break;

        case "yellow":
          // Yellow → Red
          yellowLight.classList.remove("active");
          redLight.classList.add("active");
          currentLight = "red";
          timeRemaining = timings.red;
          break;

        case "red":
          // Red → Green
          redLight.classList.remove("active");
          greenLight.classList.add("active");
          currentLight = "green";
          timeRemaining = timings.green;
          break;
      }
    }
  }, 1000);
}

function updateTimingDisplay(light, seconds) {
  const timingDisplay = document.getElementById("timing-display");
  const capitalizedLight = light.charAt(0).toUpperCase() + light.slice(1);
  timingDisplay.innerHTML = `
        <p>${capitalizedLight} light: ${seconds} seconds</p>
        <p class="timing-note">Timing adjusted based on traffic conditions</p>
    `;
}
