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

delay = 0.01
while True:
    for i in range(128):
        strip.setPixelColor(i, Color(255, 255, 255))
        strip.show()
        time.sleep(delay)

    for i in range(128):
        strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        time.sleep(delay)
