import asyncio
import subprocess
import RPi.GPIO as GPIO  # type: ignore
import time
from enum import Enum
import requests
from spotify_scraper import SpotifyClient
from youtube_search import YoutubeSearch
import os
import shutil


# import led
import utils


class States(Enum):
    WIFI = 1
    IP = 2
    OFF = 3
    ACTIVATION = 4
    DONE = 5
    USBSTICK = 6
    DOWNLOADING = 7
    SPOTIFY = 8
    DELETING = 9


STATE = {"DISPLAY": States.WIFI}
DB_CON = None
DB_CURSOR = None


async def init01_wifi():
    # Show wifi icon until connected
    while True:
        try:
            res = subprocess.run(
                ["/usr/sbin/iwgetid"], capture_output=True, text=True
            ).stdout

            if len(res) == 0:
                print("[init01] Not connected to wifi")
                await asyncio.sleep(3)
            else:
                print("[init01] Connected to wifi")
                break

        except Exception as err:
            print(err)


async def init02_loadStorage():
    # global DB_CURSOR, DB_CON

    # DB_CON = sqlite3.connect("data.db")
    # DB_CURSOR = DB_CON.cursor()
    pass


async def handle_activation():
    global STATE
    loop = asyncio.get_event_loop()

    # See if usb stick is plugged in
    STATE = {"DISPLAY": "USBSTICK"}
    while True:
        try:
            res = subprocess.run(
                ["/usr/bin/lsblk"], capture_output=True, text=True
            ).stdout

            if not "sda1" in res:
                print("[handler] Not plugged in")
                await asyncio.sleep(3)
            else:
                print("[handler] Found usb stick")
                break

        except Exception as err:
            print(err)

    # Mount usb stick
    device = "/dev/sda1"
    mount_point = "/mnt/usbstick"
    try:
        os.makedirs(mount_point, exist_ok=True)
        subprocess.run(["/usr/bin/mount", device, mount_point], check=True)
    except Exception as err:
        print(err)

    # TODO: Empty dir - Improve not needed
    STATE = {"DISPLAY": "DELETING"}

    try:
        await loop.run_in_executor(None, shutil.rmtree, mount_point + "/")
        print(f"Directory '{mount_point}' and its contents have been deleted.")
    except FileNotFoundError:
        print(f"Directory '{mount_point}' not found.")
    except OSError as e:
        print(f"Error: {e.filename} - {e.strerror}")

    # Request playlist url
    STATE = {"DISPLAY": "SPOTIFY"}

    response1 = await loop.run_in_executor(
        None, requests.get, "http://localhost:80/api/playlist"
    )
    playlistURL = response1.text

    # Extract tracks from playlist
    client = SpotifyClient()
    playlist = await loop.run_in_executor(
        None, client.get_playlist_info, playlistURL.replace('"', "")
    )
    tracks_count = playlist.get("track_count", 0)

    print("Found Tracks" + str(tracks_count))

    # Loop over tracks
    current = 0
    for track in playlist["tracks"]:
        STATE = {"DISPLAY": "DOWNLOADING", "TOTAL": tracks_count, "CURRENT": current}

        track_name = track.get("name", "Unknown")
        track_artist = (
            track.get("artists", [{}])[0].get("name", "Unknown")
            if track.get("artists")
            else "Unknown"
        )

        # Find youtube url
        results = await loop.run_in_executor(
            None,
            YoutubeSearch,
            track_name + " " + track_artist + " lyrics",
            max_results=10,
        ).to_dict()
        video_URL = "https://youtube.com" + results[0]["url_suffix"]

        print("URL for" + video_URL)

        # Download using ytdlp
        await asyncio.create_subprocess_shell(
            "./yt-dlp_linux_aarch64 -f bestaudio -x --audio-format mp3 --no-playlist -o 'out.mp3' '"
            + video_URL
            + "'",
            cwd="/home/playlogo",
        )

        print("Downlaoded")

        # Copy to stick
        shutil.copyfile(
            "/home/playlogo/out.mp3",
            mount_point
            + "/"
            + str(current).zfill(len(str(tracks_count)))
            + "_"
            + track_name
            + "_"
            + track_artist,
        )
        print("Copied")

        # Delete downloaded
        os.remove("/home/playlogo/out.mp3")
        print("Deleted")

        current += 1


async def main():
    global STATE

    # Await wifi connection
    STATE = {"DISPLAY": "WIFI"}
    await init01_wifi()

    # Display ip
    ip = utils.get_ip()
    print("IP" + ip)
    STATE = {"DISPLAY": "IP", "VALUE": ip}
    # await asyncio.sleep(10)

    # Turn off display and wait for activation
    while True:
        STATE = {"DISPLAY": "OFF"}
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
                print("[main] Button pressed")
                STATE = {"DISPLAY": "ACTIVATION"}
                await handle_activation()
                STATE = {"DISPLAY": "DONE"}
                await asyncio.sleep(10)

            await asyncio.sleep(0.2)


if __name__ == "__main__":
    # task_leds = asyncio.create_task(led.runner(STATE))
    # asyncio.run(task_leds, task_main)
    asyncio.run(main())
