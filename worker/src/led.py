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

delay = 0.01
while True:
    for i in range(128 * 10):
        strip.setPixelColor(
            math.floor(i / 10), Color(25 * (i % 128), 25 * (i % 128), 25 * (i % 128))
        )
        strip.show()
        time.sleep(delay)

    for i in range(128 * 10):
        strip.setPixelColor(
            math.floor(i / 10),
            Color(255 - 25 * (i % 128), 255 - 25 * (i % 128), 255 - 25 * (i % 128)),
        )
        strip.show()
        time.sleep(delay)
