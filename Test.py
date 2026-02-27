from flask import Flask, jsonify, render_template
from gpiozero import LED, Button
from time import time, sleep
from Speed import soc_extract
import os, threading
import serial

app = Flask(__name__)

# Images folder
IMG_FOLDER = os.path.join('static', 'img')
app.config['UPLOAD_FOLDER'] = IMG_FOLDER

# Pin definitions
ledPos = LED(6)
ledNeg = LED(22)
hallSensor = Button(26)  # Hall effect sensor pin

# =========================
# Variables
# =========================
speedMilesPerHour = 0.00
arduinoSpeed = 0.0   # <-- Arduino speed variable
startTime = 0
endTime = 0
blueLedTriggered = False
triggerCount = 0

XPos = 50
XNeg = 13
wheelRadius = 23.495  # cm
circumference = 2 * 3.141592653589793 * wheelRadius
cmToMiles = 160934
triggersPerRotation = 16

# =========================
# Speed calculation (Hall sensor)
# =========================
def calculate_speed():
    global triggerCount, startTime, endTime, speedMilesPerHour
    if triggerCount == triggersPerRotation:
        endTime = time()
        timeDiff = (endTime - startTime) / 3600
        speedCmPerSec = (circumference / cmToMiles) / timeDiff
        speedMilesPerHour = speedCmPerSec
        print(f"[HALL] Speed (mph) = {speedMilesPerHour:.01f}")
        triggerCount = 0
        startTime = endTime

# =========================
# Hall sensor handlers
# =========================
def hall_triggered():
    global blueLedTriggered, triggerCount
    ledPos.on()
    ledNeg.off()
    if not blueLedTriggered:
        blueLedTriggered = True
        triggerCount += 1

def hall_not_triggered():
    global blueLedTriggered
    ledNeg.on()
    ledPos.off()
    if blueLedTriggered:
        blueLedTriggered = False
        calculate_speed()

hallSensor.when_pressed = hall_triggered
hallSensor.when_released = hall_not_triggered

# =========================
# SOC
# =========================
def getSOC():
    soc = soc_extract.getSOC()
    return soc

# =========================
# Arduino serial thread
# =========================
def read_arduino_speed():
    global arduinoSpeed

    port = '/dev/ttyACM0'
    baudrate = 115200
    print("Intentando conectar al Arduino...")

    while True:
        try:
            ser = serial.Serial(port, baudrate, timeout=1)
            sleep(2)
            ser.flushInput()
            print("Arduino connected")
            break
        except Exception as e:
            print("Error conectando Arduino...")
            sleep(1)

    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            if line:
                print("RAW:", line)   # debug real

                # como son enteros:
                newspeed = int(line)

                # filtro suave (telemetría real)
                alpha = 0.3
                arduinoSpeed = int(arduinoSpeed + alpha * (newspeed - arduinoSpeed))

                print(f"[ARDUINO] Speed: {arduinoSpeed}")

        except Exception as e:
            print("Error leyendo serial:", e)

# =========================
# Routes
# =========================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/speed')
def speed():
    print("Enviando velocidad:", arduinoSpeed)
    return jsonify(speed=arduinoSpeed)

@app.route('/arduino_speed')
def arduino_speed():
    return jsonify(speed=int(round(arduinoSpeed)))

@app.route("/soc")
def soc():
    return jsonify(soc=getSOC())

# =========================
# Main
# =========================
if __name__ == "__main__":
    soc_extract.login()

    # Start Arduino reader thread
    arduino_thread = threading.Thread(target=read_arduino_speed, daemon=True)
    arduino_thread.start()

    try:
        startTime = time()
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("Program interrupted by user")
        soc_extract.exit()