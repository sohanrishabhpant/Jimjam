import RPi.GPIO as GPIO
import time
import json
from config import *

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(R_PIN, GPIO.OUT)
GPIO.setup(G_PIN, GPIO.OUT)
GPIO.setup(B_PIN, GPIO.OUT)

R_PWM = GPIO.PWM(R_PIN, 100)
G_PWM = GPIO.PWM(G_PIN, 100)
B_PWM = GPIO.PWM(B_PIN, 100)

R_PWM.start(100)
G_PWM.start(100)
B_PWM.start(100)

TS_COLORS = {
    0: {"name": "red", "pins": R_PIN, "pwm": R_PWM},
    1: {"name": "green", "pins": G_PIN, "pwm": G_PWM},
    2: {"name": "blue", "pins": B_PIN, "pwm": B_PWM},
    3: {"name": "yellow", "pins": (R_PIN, G_PIN), "pwm": (R_PWM, G_PWM)},
    4: {
        "name": "white",
        "pins": (R_PIN, G_PIN, B_PIN),
        "pwm": (R_PWM, G_PWM, B_PWM),
    },
    5: {
        "name": "all",
        "pins": (R_PIN, G_PIN, B_PIN),
        "pwm": (R_PWM, G_PWM, B_PWM),
    },
}

PREV_TIME = ""

data = {}
status = -1
while True:
    with open("status.txt", "r") as f:
        x = f.read()
        if(x!=''):
            status = int(x)

    if status != 2:
        continue

    with open("xinfo.txt","r") as f:
        data = json.load(f);
    
    TIME = data["created_at"]
    if TIME == PREV_TIME:
        continue
    ITERATIONS = int(data["field1"])
    DURATION = float(data["field2"])
    DELAY = float(data["field3"])
    INTENSITY = int(data["field4"])
    print(data["field5"])
    COLOR_NAME = TS_COLORS[int(data["field5"])]["name"]
    COLOR_PINS = TS_COLORS[int(data["field5"])]["pins"]
    COLOR_PWMS = TS_COLORS[int(data["field5"])]["pwm"]
    
    print("Patient in well lit room....")
    time.sleep(60)
    with open("foo.txt", "a") as f:
        f.write("?,")
    print("Patient in dark room....")
    time.sleep(60)
    with open("foo.txt", "a") as f:
        f.write("?,")

    print(
        f"[$] {ITERATIONS} iterations of {INTENSITY}% {COLOR_NAME} for {DURATION}s with {DELAY}s delay"
    )
    
    if COLOR_NAME == "all":
        for id, color in TS_COLORS.items():
            if id != 5:
                COLOR_PINS = TS_COLORS[id]["pins"]
                COLOR_PWMS = TS_COLORS[id]["pwm"]
                for _ in range(ITERATIONS):
                    print(f"[$] Starting iteration {_ + 1}")
                    if isinstance(COLOR_PWMS, tuple):
                        for COLOR_PWM in COLOR_PWMS:
                            COLOR_PWM.ChangeDutyCycle(0)
                    else:
                        COLOR_PWMS.ChangeDutyCycle(0)

                    time.sleep(DURATION)

                    if isinstance(COLOR_PWMS, tuple):
                        for COLOR_PWM in COLOR_PWMS:
                            COLOR_PWM.ChangeDutyCycle(100)
                    else:
                        COLOR_PWMS.ChangeDutyCycle(100)

                    time.sleep(DELAY)
                with open("foo.txt", "a") as f:
                    f.write("?,")
                if id != 4:
                    print("Changing Colour....")
                    time.sleep(30)
                    with open("foo.txt", "a") as f:
                    f.write("?,")
                
        PREV_TIME = TIME
        with open("status.txt", "w") as f:
            f.write("3")

        R_PWM.start(100)
        G_PWM.start(100)
        B_PWM.start(100)

        time.sleep(1)

    else: 
        for _ in range(ITERATIONS):
            print(f"[$] Starting iteration {_ + 1}")
            if isinstance(COLOR_PWMS, tuple):
                for COLOR_PWM in COLOR_PWMS:
                    COLOR_PWM.ChangeDutyCycle(100 - INTENSITY)
            else:
                COLOR_PWMS.ChangeDutyCycle(100 - INTENSITY)

            time.sleep(DURATION)

            if isinstance(COLOR_PWMS, tuple):
                for COLOR_PWM in COLOR_PWMS:
                    COLOR_PWM.ChangeDutyCycle(100)
            else:
                COLOR_PWMS.ChangeDutyCycle(100)
            time.sleep(DELAY)
            with open("foo.txt", "a") as f:
                    f.write("?")

        PREV_TIME = TIME

        with open("status.txt", "w") as f:
            f.write("3")

        R_PWM.start(100)
        G_PWM.start(100)
        B_PWM.start(100)

        time.sleep(1)

