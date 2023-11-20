from flask import Flask, render_template
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import cv2
import time
import requests

app = Flask(__name__)

R_PIN = 11  # Physical Pin 11
G_PIN = 13  # Physical Pin 13
B_PIN = 15  # Physical Pin 15

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(R_PIN, GPIO.OUT)
GPIO.setup(G_PIN, GPIO.OUT)
GPIO.setup(B_PIN, GPIO.OUT)

RED_PWM = GPIO.PWM(R_PIN, 100)  # 100 Hz frequency
GREEN_PWM = GPIO.PWM(G_PIN, 100)
BLUE_PWM = GPIO.PWM(B_PIN, 100)

def turn_on_color(color, intensity):
    intensity = max(0, min(100, 100 - int(intensity)))
    duty_cycle = intensity

    if color == "r":
        RED_PWM.start(duty_cycle)
        GREEN_PWM.start(100)
        BLUE_PWM.start(100)
    elif color == "g":
        RED_PWM.start(100)
        GREEN_PWM.start(duty_cycle)
        BLUE_PWM.start(100)
    elif color == "b":
        RED_PWM.start(100)
        GREEN_PWM.start(100)
        BLUE_PWM.start(duty_cycle)
    elif color == "y":
        RED_PWM.start(duty_cycle)
        GREEN_PWM.start(duty_cycle)
        BLUE_PWM.start(100)
    elif color == "w":
        RED_PWM.start(duty_cycle)
        GREEN_PWM.start(duty_cycle)
        BLUE_PWM.start(duty_cycle)
    elif color == "off":
        RED_PWM.start(100)
        GREEN_PWM.start(100)
        BLUE_PWM.start(100)

def calibrate_and_generate_graph(color, intensity):
    turn_on_color(color, intensity)

    # Your existing calibration code goes here
    # ...

    # Generate the graph
    plt.plot(times1, radii1)
    plt.xlabel('Time (s)')
    plt.ylabel('Radius')

    # Save the graph to a BytesIO object
    graph_stream = BytesIO()
    plt.savefig(graph_stream, format='png')
    graph_stream.seek(0)

    # Convert the BytesIO object to a base64-encoded string
    graph_base64 = base64.b64encode(graph_stream.read()).decode('utf-8')

    # Close the plot to prevent it from being displayed on the server
    plt.close()

    return graph_base64

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/calibrate/<color>/<intensity>')
def calibrate(color, intensity):
    graph_base64 = calibrate_and_generate_graph(color, intensity)
    return render_template('calibration.html', graph_base64=graph_base64)

@app.route("/control/<color>/<intensity>")
def control(color, intensity):
    turn_on_color(color, intensity)
    return f"Turning on {color} LED with intensity {intensity}"

if __name__ == '__main__':
    app.run(debug=True)
