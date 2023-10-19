import RPi.GPIO as GPIO
import time

# Define GPIO pin
GPIO_PIN = 27  # Change this to your GPIO pin

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

try:
    while True:
        # Wait for a rising edge
        GPIO.wait_for_edge(GPIO_PIN, GPIO.RISING)
        pulse_count += 1

        # Calculate time elapsed
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Reset the count and time if a second has passed
        if elapsed_time >= 1.0:
            speed_mph = (pulse_count / PULSES_PER_ROTATION) * (2 * 3.14159 * WHEEL_RADIUS_M) / elapsed_time * METERS_TO_MILES
            print(f"Speed: {speed_mph:.2f} mph")

            pulse_count = 0
            start_time = time.time()

except KeyboardInterrupt:
    print("Measurement stopped by user")

finally:
    GPIO.cleanup()
