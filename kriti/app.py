from flask import Flask, render_template
import RPi.GPIO as GPIO
import sys

app = Flask(__name__)

R_PIN = 11  # Physical Pin 11
G_PIN = 13  # Physical Pin 13
B_PIN = 15  # Physical Pin 15

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(R_PIN, GPIO.OUT)
GPIO.setup(G_PIN, GPIO.OUT)
GPIO.setup(B_PIN, GPIO.OUT)

def turn_on_color(color):
    if color == "r":
        GPIO.output(R_PIN, 0)
        GPIO.output(G_PIN, 1)
        GPIO.output(B_PIN, 1)
    elif color == "g":
        GPIO.output(R_PIN, 1)
        GPIO.output(G_PIN, 0)
        GPIO.output(B_PIN, 1)
    elif color == "b":
        GPIO.output(R_PIN, 1)
        GPIO.output(G_PIN, 1)
        GPIO.output(B_PIN, 0)
    elif color == "y":
        GPIO.output(R_PIN, 0)
        GPIO.output(G_PIN, 0)
        GPIO.output(B_PIN, 1)
    elif color == "w":
        GPIO.output(R_PIN, 0)
        GPIO.output(G_PIN, 0)
        GPIO.output(B_PIN, 0)
    elif color == "off":
        GPIO.output(R_PIN, 1)
        GPIO.output(G_PIN, 1)
        GPIO.output(B_PIN, 1)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/control/<color>")
def control(color):
    turn_on_color(color)
    return f"Turning on {color} LED"

if __name__ == "__main__":
    app.run(debug=True)
