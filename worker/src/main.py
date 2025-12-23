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

# import asyncio
# import subprocess
# import sqlite3


# import led

# STATE = {"DISPLAY": "WIFI"}
# DB_CON = None
# DB_CURSOR = None


# async def init01_wifi():
#     # Show wifi icon until connected
#     while True:
#         try:
#             res = subprocess.run(["ls", "-l"], capture_output=True, text=True).stdout

#             if len(res) == 0:
#                 asyncio.sleep(3)
#             else:
#                 break

#         except Exception as err:
#             print(err)


# async def init02_loadStorage():
#     global DB_CURSOR, DB_CON

#     DB_CON = sqlite3.connect("data.db")
#     DB_CURSOR = DB_CON.cursor()


# async def main():
#     global STATE

#     STATE = {"DISPLAY": "WIFI"}
#     await init01_wifi()

#     STATE = {"DISPLAY": "STORAGE"}
#     await init02_loadStorage()


# if __name__ == "__main__":
#     task_leds = asyncio.create_task(led.runner(STATE))
#     task_main = asyncio.create_task(main())
#     asyncio.run(task_leds, task_main)
