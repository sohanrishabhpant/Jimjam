import sys
import RPi.GPIO as GPIO

R_PIN = 11  # Physical Pin 11
G_PIN = 13  # Physical Pin 13
B_PIN = 15  # Physical Pin 15

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(R_PIN, GPIO.OUT)
GPIO.setup(G_PIN, GPIO.OUT)
GPIO.setup(B_PIN, GPIO.OUT)

if sys.argv[1] == "r":
    GPIO.output(R_PIN, 0)
    GPIO.output(G_PIN, 1)
    GPIO.output(B_PIN, 1)
elif sys.argv[1] == "g":
    GPIO.output(R_PIN, 1)
    GPIO.output(G_PIN, 0)
    GPIO.output(B_PIN, 1)
elif sys.argv[1] == "b":
    GPIO.output(R_PIN, 1)
    GPIO.output(G_PIN, 1)
    GPIO.output(B_PIN, 0)
elif sys.argv[1] == "y":
    GPIO.output(R_PIN, 0)
    GPIO.output(G_PIN, 0)
    GPIO.output(B_PIN, 1)
elif sys.argv[1] == "w":
    GPIO.output(R_PIN, 0)
    GPIO.output(G_PIN, 0)
    GPIO.output(B_PIN, 0)
elif sys.argv[1] == "0":
    GPIO.output(R_PIN, 1)
    GPIO.output(G_PIN, 1)
    GPIO.output(B_PIN, 1)
