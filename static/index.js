// Create a variable to store the main gear
let mainGear = "D";

// Function to switch properties between gears
function switchProperties(gear) {
  // Get the main and selected gear elements
  const mainElement = document.querySelector(`[data-gear="${mainGear}"]`);
  const selectedElement = document.querySelector(`[data-gear="${gear}"]`);

  // Store the styles of the main gear
  const mainStyles = {
    position: getComputedStyle(mainElement).getPropertyValue("position"),
    fontSize: getComputedStyle(mainElement).getPropertyValue("font-size"),
    opacity: getComputedStyle(mainElement).getPropertyValue("opacity"),
    left: getComputedStyle(mainElement).getPropertyValue("left"),
    top: getComputedStyle(mainElement).getPropertyValue("top"),
  };

  // Store the styles of the selected gear
  const selectedStyles = {
    position: getComputedStyle(selectedElement).getPropertyValue("position"),
    fontSize: getComputedStyle(selectedElement).getPropertyValue("font-size"),
    opacity: getComputedStyle(selectedElement).getPropertyValue("opacity"),
    left: getComputedStyle(selectedElement).getPropertyValue("left"),
    top: getComputedStyle(selectedElement).getPropertyValue("top"),
  };

  // Apply the styles of the selected gear to the main gear
  mainElement.style.position = selectedStyles.position;
  mainElement.style.fontSize = selectedStyles.fontSize;
  mainElement.style.opacity = selectedStyles.opacity;
  mainElement.style.left = selectedStyles.left;
  mainElement.style.top = selectedStyles.top;

  // Apply the styles of the main gear to the selected gear
  selectedElement.style.position = mainStyles.position;
  selectedElement.style.fontSize = mainStyles.fontSize;
  selectedElement.style.opacity = mainStyles.opacity;
  selectedElement.style.left = mainStyles.left;
  selectedElement.style.top = mainStyles.top;

  // Update the main gear variable
  mainGear = gear;
}

// Keyboard event listener to toggle gears
document.addEventListener("keydown", (event) => {
  const key = event.key.toUpperCase();
  if (key === "R" || key === "N" || key === "D") {
    switchProperties(key);
  }
});

// Track the state of arrow key toggles
let leftArrowToggled = false;
let rightArrowToggled = false;
let isBlinking = false;
let blinkInterval;

// Function to start or stop arrow blinking based on the state
function toggleArrowBlinking(className, toggleState) {
  const arrowElement = document.querySelector(className);
  if (toggleState) {
    arrowElement.classList.add("blinking");
  } else {
    arrowElement.classList.remove("blinking");
  }
}

// Keyboard event listener to toggle arrow blinking
document.addEventListener("keydown", (event) => {
  if (event.key === "ArrowLeft") {
    if (!leftArrowToggled) {
      // Start blinking for left arrow
      toggleArrowBlinking(".left-arrow", true);
      toggleArrowBlinking(".right-arrow", false); // Stop blinking for right arrow
      leftArrowToggled = true;
      rightArrowToggled = false;
    } else {
      // Toggle blinking for left arrow
      toggleArrowBlinking(".left-arrow", false);
      leftArrowToggled = false;
    }
  } else if (event.key === "ArrowRight") {
    if (!rightArrowToggled) {
      // Start blinking for right arrow
      toggleArrowBlinking(".right-arrow", true);
      toggleArrowBlinking(".left-arrow", false); // Stop blinking for left arrow
      rightArrowToggled = true;
      leftArrowToggled = false;
    } else {
      // Toggle blinking for right arrow
      toggleArrowBlinking(".right-arrow", false);
      rightArrowToggled = false;
    }
  } else {
    // If any other key is pressed, stop blinking for both arrows
    if (leftArrowToggled || rightArrowToggled) {
      toggleArrowBlinking(".left-arrow", false);
      toggleArrowBlinking(".right-arrow", false);
      leftArrowToggled = false;
      rightArrowToggled = false;
    }
  }
});

// Keyboard event listener to toggle lights
document.addEventListener("keydown", (event) => {
  if (event.key === "C") {
    // Toggle low beam headlights
    const lowBeamHeadlights = document.querySelectorAll(".low-beam-headlights");
    lowBeamHeadlights.forEach((headlight) => {
      headlight.style.display =
        headlight.style.display === "none" ? "block" : "none";
    });
  } else if (event.key === "I") {
    // Toggle parking lights
    const parkingLights = document.querySelectorAll(".parking-lights");
    parkingLights.forEach((parkingLight) => {
      parkingLight.style.display =
        parkingLight.style.display === "none" ? "block" : "none";
    });

    // Toggle both arrows
    const leftArrow = document.querySelector(".left-arrow");
    const rightArrow = document.querySelector(".right-arrow");

    if (!isBlinking) {
      isBlinking = true;

      blinkInterval = setInterval(() => {
        toggleArrowBlinking(".left-arrow", true);
        toggleArrowBlinking(".right-arrow", true);
      });
    } else {
      isBlinking = false;
      clearInterval(blinkInterval); // Stop the blinking interval
      toggleArrowBlinking(".left-arrow", false);
      toggleArrowBlinking(".right-arrow", false);
    }
  } else if (event.key === "A") {
    // Toggle lights
    const lights = document.querySelectorAll(".lights");
    lights.forEach((light) => {
      light.style.display = light.style.display === "none" ? "block" : "none";
    });
  }
});

function updateVelocity() {
  fetch("/speed")
    .then((response) => response.json())
    .then((data) => {
      document.getElementById("velocity").innerText = data.speed;
    })
    .catch((error) => console.error(error));
}

// Function to update battery charge (text-wrapper-12) gradually
function updateBatteryCharge() {
  fetch("/soc")
    .then((response) => response.json())
    .then((data) => {
      // Update the HTML element with the current battery charge
      document.getElementById("soc").innerText = data.soc;
    })
    .catch((error) => console.error(error));
}

function updateDate() {
  var date = new Date();
  var hour = date.getHours();
  var minute = date.getMinutes();
  var day = date.getDate();
  var month = date.getMonth() + 1;
  var year = date.getFullYear();

  document.querySelector(".text-wrapper").textContent = hour + ":" + minute;
  document.querySelector(".text-wrapper-2").textContent =
    month + "/" + day + "/" + year;
}

function updateBatteryColor() {
  var battery_ring = document.querySelector(".battery-ring");
  var currentCharge = parseInt(document.getElementById("soc").innerText);

  if (currentCharge >= 75) {
    battery_ring.src = "static/img/battery-ring.svg";
  } else if (currentCharge >= 40 && currentCharge < 75) {
    battery_ring.src = "static/img/battery-ring-y.svg";
  } else {
    battery_ring.src = "static/img/battery-ring-r.svg";
  }
}

function updateRangeColor() {
  var range_bar = document.querySelector(".range-bar");
  var currentVelocity = document.querySelector(".text-wrapper-4");
  var currentVelocityNumber = parseFloat(
    document.querySelector(".text-wrapper-4").textContent
  );
  var currentOptimalVelocity = parseFloat(
    document.querySelector(".element-optvel").querySelector("em").textContent
  );

  if (
    currentVelocityNumber > currentOptimalVelocity + 5 ||
    currentVelocityNumber < currentOptimalVelocity - 5
  ) {
    range_bar.src = "static/img/range-bar-r.svg";
    currentVelocity.style.color = "#ea0000";
  } else if (
    currentVelocityNumber > currentOptimalVelocity + 3 ||
    currentVelocityNumber < currentOptimalVelocity - 3
  ) {
    range_bar.src = "static/img/range-bar-y.svg";
    currentVelocity.style.color = "#ead700";
  } else {
    range_bar.src = "static/img/range-bar.svg";
    currentVelocity.style.color = "#01EB7B";
  }
}

function updateOptimalVelocity() {
  var currentOptimalVelocity = parseFloat(
    document.querySelector(".element-optvel").querySelector("em").textContent
  );
  var targetOptimalVelocity = Math.floor(Math.random() * 100); // Generate a random target velocity
  var step = 1; // Adjust the step size for the transition speed

  // Gradually transition to the target velocity
  if (targetOptimalVelocity > currentOptimalVelocity) {
    currentOptimalVelocity = Math.min(
      currentOptimalVelocity + step,
      targetOptimalVelocity
    );
  } else if (targetOptimalVelocity < currentOptimalVelocity) {
    currentOptimalVelocity = Math.max(
      currentOptimalVelocity - step,
      targetOptimalVelocity
    );
  }

  // Update the HTML element with the current velocity
  document.querySelector(".element-optvel").querySelector("em").textContent =
    currentOptimalVelocity;
  document.querySelector(".text-wrapper-10").querySelector("em").textContent =
    currentOptimalVelocity;
}

// Call the updateValues function initially
updateVelocity();
updateBatteryCharge();
updateBatteryColor();
updateOptimalVelocity();
updateRangeColor();
updateDate();

// Set intervals to update values gradually every second
setInterval(updateDate, 1000);
setInterval(updateVelocity, 1500); // Change every second for velocity
setInterval(updateRangeColor, 1000);
setInterval(updateBatteryCharge, 1000); // Change every second for battery charge
setInterval(updateBatteryColor, 1000); // Change every 4 seconds for battery charge
setInterval(updateOptimalVelocity, 4000); // Change every 4 seconds for optimal velocity
