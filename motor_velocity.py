import RPi.GPIO as GPIO
import time

# Constants for calculation
PULSES_PER_ROTATION = 48
WHEEL_RADIUS_M = 0.24
METERS_TO_MILES = 0.000621371  # Conversion factor for meters to miles

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Variables for pulse counting
pulse_count = 0
start_time = time.time()

while True:
    try:
        # Wait for a rising edge
        GPIO.wait_for_edge(GPIO_PIN, GPIO.RISING)
        pulse_count += 1

        # Calculate time elapsed
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Reset the count and time if a second has passed
        if elapsed_time >= 1.0:
            speed_mph = (pulse_count / PULSES_PER_ROTATION) * WHEEL_RADIUS_M
            velocity = (
                speed_mph * METERS_TO_MILES * 1609.34
            )  # convert to meters per second

            print str(velocity)  # Return the velocity as a string

            pulse_count = 0
            start_time = time.time()

    except KeyboardInterrupt:
        print("Measurement stopped by the user")

    finally:
        GPIO.cleanup()
