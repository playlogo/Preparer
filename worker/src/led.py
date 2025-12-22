import threading
import time
import RPi.GPIO as GPIO  # type: ignore

from rpi_ws281x import PixelStrip, Color  # type: ignore
from lib.config import config
from lib.ipc.client_async import IPCClientAsync

from hardware.lib.canvas import Canvas
from hardware.lib.consts import COLOR_ORANGE, COLOR_PURPLE, FPS, COLOR_NEON_GREEN
from hardware.lib.point import Point
from hardware.lib.point_effects import FadeOutEffect
from hardware.lib.show import effect_lookup, canvas_thread_lock
from hardware.lib.lookup import lookup
import sys
import logging

log = logging.getLogger("aether")
log.addHandler(logging.StreamHandler(sys.stdout))
log.setLevel(logging.DEBUG)
import asyncio


class Hardware:
    active_effects = {}
    previous_effect = None
    startupEffect = None

    def __init__(self):
        # Setup canvas
        self._init_canvas()

    def _init_canvas(self):
        self.FPS = FPS

        # Create strip object
        self.strip = PixelStrip(
            33,
            config["hardware"]["ledPin"],
            800000,
            10,
            False,
            200,
            0,
        )

        self.strip.begin()

        # Create canvas
        canvas = Canvas()
        self.canvas = canvas

        # Play startup animation
        effect = effect_lookup["startup"](self.canvas, self.previous_effect)
        effect.create()
        self.active_effects["startup"] = effect

    async def run_render_in_thread(self):
        while True:
            start_time = time.time()

            # Execute your render function
            with canvas_thread_lock:
                self.canvas.tick()
                self.stripHandler(self.canvas.render())

            # Calculate how long to sleep to maintain 60 FPS
            elapsed_time = time.time() - start_time
            time_to_sleep = max(0.01, (1 / self.FPS) - elapsed_time)
            await asyncio.sleep(time_to_sleep)

            if elapsed_time > 1 / self.FPS:
                # log.info("Frame took too long to render:", elapsed_time)
                pass

    def stripHandler(self, array):
        index = 0

        for y in array[0]:
            ledIndex = lookup[index]
            index += 1

            if ledIndex != 0:
                self.strip.setPixelColor(
                    ledIndex - 1,
                    Color(
                        max(0, min(255, int(y[0]))),
                        max(0, min(255, int(y[1]))),
                        max(0, min(255, int(y[2]))),
                    ),
                )

        for y in reversed(array[3]):
            ledIndex = lookup[index]
            index += 1

            if ledIndex != 0:
                self.strip.setPixelColor(
                    ledIndex - 1,
                    Color(
                        max(0, min(255, int(y[0]))),
                        max(0, min(255, int(y[1]))),
                        max(0, min(255, int(y[2]))),
                    ),
                )

        for y in array[7]:
            ledIndex = lookup[index]
            index += 1

            if ledIndex != 0:
                self.strip.setPixelColor(
                    ledIndex - 1,
                    Color(
                        max(0, min(255, int(y[0]))),
                        max(0, min(255, int(y[1]))),
                        max(0, min(255, int(y[2]))),
                    ),
                )

        for y in reversed(array[10]):
            ledIndex = lookup[index]
            index += 1

            if ledIndex != 0:
                self.strip.setPixelColor(
                    ledIndex - 1,
                    Color(
                        max(0, min(255, int(y[0]))),
                        max(0, min(255, int(y[1]))),
                        max(0, min(255, int(y[2]))),
                    ),
                )

        self.strip.show()

    async def loop(self):
        ipc_client = IPCClientAsync()
        await ipc_client.connect()

        log.debug("[hardware] Loop started")

        try:
            while True:
                topic, data = await ipc_client.receive()

                if topic == "create_effect":
                    effect = effect_lookup[data["effectType"]](
                        self.canvas, self.previous_effect
                    )
                    effect.create()

                    self.active_effects[data["effectID"]] = effect

                if topic == "delete_effect":
                    effect = self.active_effects[data["effectID"]]
                    effect.remove()

                    self.previous_effect = effect

                    del self.active_effects[data["effectID"]]

        except KeyboardInterrupt:
            log.debug("[hardware] Loop stopped")
            GPIO.cleanup()

    async def button_handler(self):
        ipc_client = IPCClientAsync()
        await ipc_client.connect()

        GPIO.setmode(GPIO.BCM)

        # Configure inputs
        GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
        GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
        GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

        debounced = [0, 0, 0]
        debounce_time = 2

        # Check buttons every 0.1 seconds, debounce for 2 seconds
        while True:
            if GPIO.input(23) == GPIO.LOW:
                if (debounced[0] + debounce_time) > time.time():
                    continue

                debounced[0] = time.time()

                log.debug("[hardware] Top Button pressed")

                await ipc_client.publish("button_top_pressed")

                self.button_feedback(0, COLOR_ORANGE)

                log.info("[hardware] Top Button pressed")

            if GPIO.input(25) == GPIO.LOW:
                if (debounced[1] + 5) > time.time():
                    continue

                debounced[1] = time.time()

                log.debug("[hardware] Middle Button pressed")

                await ipc_client.publish("button_middle_pressed")

                log.info("[hardware] Middle Button pressed")

            if GPIO.input(24) == GPIO.LOW:
                if (debounced[2] + debounce_time) > time.time():
                    continue

                debounced[2] = time.time()

                log.debug("[hardware] Bottom Button pressed")

                await ipc_client.publish("button_bottom_pressed")

                self.button_feedback(2, COLOR_PURPLE)

                log.info("[hardware] Bottom Button pressed")

            await asyncio.sleep(0.1)

    def button_feedback(self, button, color):
        # Create new point at button position
        point = Point(
            1.5,
            1,
            color,
            3 if button == 0 or button == 2 else 0,
            180 if button == 0 else 0,
            [FadeOutEffect(0.5, delete=True)],
            overlay=True,
            group="button_feedback",
        )

        self.canvas.points.append(point)
