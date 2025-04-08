from flask import Flask, jsonify, render_template
from gpiozero import LED, Button
from time import time, sleep
from Speed import soc_extract
import os, threading


app = Flask(__name__)

#Images folder
IMG_FOLDER = os.path.join('static', 'img')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER

# Pin definitions
ledPos = LED(6)
ledNeg = LED(22)
hallSensor = Button(26)  # Pin to which the hall effect sensor is connected

# Variables
speedMilesPerHour = 0.00
startTime = 0
endTime = 0
blueLedTriggered = False
triggerCount = 0  # Count of triggers

XPos = 50
XNeg = 13
wheelRadius = 23.495  # wheel radius in centimeters
circumference = 2 * 3.141592653589793 * wheelRadius  # wheel circumference in centimeters
cmToMiles = 160934  # conversion factor from cm to miles
triggersPerRotation = 16  # Number of triggers for one full rotation


# getComputedStyle
# Function to calculate and print speed
def calculate_speed():
    global triggerCount, startTime, endTime, speedMilesPerHour
    if triggerCount == triggersPerRotation:
        endTime = time()  # Get the current time in seconds
        timeDiff = (endTime - startTime) / 3600  # Convert time to hours
        speedCmPerSec = (circumference / cmToMiles) / timeDiff  # Speed = distance/time
        speedMilesPerHour = speedCmPerSec  # Convert cm/s to miles/hour
        print(f"Speed (mph) = {speedMilesPerHour:.01f}")
        triggerCount = 0  # Reset trigger count for the next rotation
        startTime = endTime  # Reset the start time

# Hall sensor event handlers
def hall_triggered():
    global blueLedTriggered, triggerCount
    ledPos.on()
    ledNeg.off()
    if not blueLedTriggered:  # Start measuring time when triggered
        blueLedTriggered = True
        triggerCount += 1  # Increment trigger count

def hall_not_triggered():
    global blueLedTriggered
    ledNeg.on()
    ledPos.off()
    if blueLedTriggered:  # Stop measuring when no longer triggered
        blueLedTriggered = False
        calculate_speed()

def getSOC():
    soc = soc_extract.getSOC()
    return soc

# Assign event handlers
hallSensor.when_pressed = hall_triggered
hallSensor.when_released = hall_not_triggered

# Route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to get the speed data
@app.route('/speed')
def speed():
    return jsonify(speed=round(speedMilesPerHour,1))

# Route to get State Of Charge
@app.route("/soc")
def soc():
    return jsonify(soc=getSOC())

# Main loop
if __name__ == "__main__":
    soc_extract.login()
    try:
        startTime = time()  # Initialize start time
        app.run(host='0.0.0.0', port=5000)  # Run the Flask app

        while True:
            sleep(0.1)  # Add a short delay to reduce CPU usage

    except KeyboardInterrupt:
        print("Program interrupted by user")
        soc_extract.exit()
