import RPi.GPIO as GPIO
import asyncio
import time
import websockets

# Define GPIO pin
GPIO_PIN = 27  # Change this to your GPIO pin

# Constants for calculation
PULSES_PER_ROTATION = 48
WHEEL_RADIUS_M = 0.24

# Variables for pulse counting
pulse_count = 0
start_time = time.time()

async def speed_measurement(websocket, path):
    while True:
        await asyncio.sleep(1)  # Update speed every second

        speed_mph = (pulse_count / PULSES_PER_ROTATION) * WHEEL_RADIUS_M * 2.237  # Convert to mph
        await websocket.send(f"Speed: {speed_mph:.2f} mph")

def gpio_callback(channel):
    global pulse_count
    pulse_count += 1

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(GPIO_PIN, GPIO.RISING, callback=gpio_callback)

    start_server = websockets.serve(speed_measurement, "0.0.0.0", 5678)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Measurement stopped by user")

    finally:
        GPIO.cleanup()
