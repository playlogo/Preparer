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

while True:
    for i in range(128):
        for brightness in range(5):
            strip.setPixelColor(
                i, Color(25 * brightness, 25 * brightness, 25 * brightness)
            )
            strip.show()

    for i in range(128):
        for brightness in range(5):
            strip.setPixelColor(
                i,
                Color(
                    255 - 25 * brightness, 255 - 25 * brightness, 255 - 25 * brightness
                ),
            )
            strip.show()
