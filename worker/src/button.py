import RPi.GPIO as GPIO  # type: ignore
import time

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
