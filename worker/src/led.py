from rpi_ws281x import PixelStrip, Color  # type: ignore
import RPi.GPIO as GPIO  # type: ignore

strip = PixelStrip(
    128,
    12,
    800000,
    10,
    False,
    200,
    0,
)

strip.begin()

import time


def run():
    delay = 0.001
    while True:
        for i in range(128):
            for brightness in range(1, 3):
                strip.setPixelColor(
                    i, Color(127 * brightness, 127 * brightness, 127 * brightness)
                )
                strip.show()
                time.sleep(delay)

        for i in range(128):
            for brightness in range(1, 3):
                strip.setPixelColor(
                    i,
                    Color(
                        255 - 127 * brightness,
                        255 - 127 * brightness,
                        255 - 127 * brightness,
                    ),
                )
                strip.show()
                time.sleep(delay)


run()

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

debounced = 0
debounce_time = 2

# Check buttons every 0.1 seconds, debounce for 2 seconds
while True:
    if GPIO.input(18) == GPIO.HIGH:
        if (debounced + debounce_time) > time.time():
            continue

        debounced = time.time()
        print("[hardware] Top Button pressed")
        run()
