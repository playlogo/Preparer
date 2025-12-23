from rpi_ws281x import PixelStrip, Color  # type: ignore

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
import math

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
