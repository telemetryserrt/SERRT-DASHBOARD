from gpiozero import LED, Button
from time import time, sleep
from flask import Flask, render_template, jsonify

# Pin definitions
ledPos = LED(6)
ledNeg = LED(22)
hallSensor = Button(26)  # Pin to which the hall effect sensor is connected

# Flask application
app = Flask(__name__)

# Variables
val = 0
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

# Function to calculate and print speed
def calculate_speed():
    global triggerCount, startTime, endTime
    if triggerCount == triggersPerRotation:
        endTime = time()  # Get the current time in seconds
        timeDiff = (endTime - startTime) / 3600  # Convert time to hours
        speedCmPerSec = (circumference / cmToMiles) / timeDiff  # Speed = distance/time
        speedMilesPerHour = speedCmPerSec  # Convert cm/s to miles/hour
        print(f"Speed (mph) = {speedMilesPerHour:.10f}")
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

# Assign event handlers
hallSensor.when_pressed = hall_triggered
hallSensor.when_released = hall_not_triggered

# # Main loop
# try:
#     startTime = time()  # Initialize start time
#     while True:
#         sleep(0.1)  # Add a short delay to reduce CPU usage

# except KeyboardInterrupt:
#     print("Program interrupted by user")


# from gpiozero import LED, Button
# from time import time, sleep
# from flask import Flask, render_template, jsonify

# # Pin definitions
# ledPos = LED(6)
# ledNeg = LED(22)
# hallSensor = Button(26)  # Pin to which the hall effect sensor is connected

# # Flask application
# app = Flask(__name__)

# # Global variables for speed and LED statuses
# val = 0
# startTime = 0
# endTime = 0
# blueLedTriggered = False
# triggerCount = 0  # Count of triggers
# current_speed = 0.0  # Store current speed
# led_status = {'positive': False, 'negative': True}  # LED statuses

# XPos = 50
# XNeg = 13
# wheelRadius = 23.495  # wheel radius in centimeters
# circumference = 2 * 3.141592653589793 * wheelRadius  # wheel circumference in centimeters
# cmToMiles = 160934  # conversion factor from cm to miles
# triggersPerRotation = 16  # Number of triggers for one full rotation

# # Function to calculate and print speed
# def calculate_speed():
#     global triggerCount, startTime, endTime, current_speed
#     if triggerCount == triggersPerRotation:
#         endTime = time()  # Get the current time in seconds
#         timeDiff = (endTime - startTime) / 3600  # Convert time to hours
#         speedCmPerSec = (circumference / cmToMiles) / timeDiff  # Speed = distance/time
#         current_speed = speedCmPerSec  # Store current speed
#         print(f"Speed (mph) = {current_speed:.10f}")
#         triggerCount = 0  # Reset trigger count for the next rotation
#         startTime = endTime  # Reset the start time

# # Hall sensor event handlers
# def hall_triggered():
#     global blueLedTriggered, triggerCount, led_status
#     ledPos.on()
#     ledNeg.off()
#     led_status['positive'] = True
#     led_status['negative'] = False
#     if not blueLedTriggered:  # Start measuring time when triggered
#         blueLedTriggered = True
#         triggerCount += 1  # Increment trigger count

# def hall_not_triggered():
#     global blueLedTriggered, led_status
#     ledNeg.on()
#     ledPos.off()
#     led_status['negative'] = True
#     led_status['positive'] = False
#     if blueLedTriggered:  # Stop measuring when no longer triggered
#         blueLedTriggered = False
#         calculate_speed()

# # Assign event handlers
# hallSensor.when_pressed = hall_triggered
# hallSensor.when_released = hall_not_triggered

# Flask route for the dashboard
@app.route('/')
def dashboard():
    return render_template('index.html')

# API route to get current speed and LED status
@app.route('/speed')
def status():
    return jsonify(speed=speedMilesPerHour)

# Start Flask app in a separate thread
from threading import Thread

def run_flask():
    app.run(host='0.0.0.0', port=5000)

# Main loop
if __name__ == '__main__':
    startTime = time()  # Initialize start time
    Thread(target=run_flask).start()  # Start the Flask app

    try:
        while True:
            sleep(0.1)  # Add a short delay to reduce CPU usage

    except KeyboardInterrupt:
        print("Program interrupted by user")
