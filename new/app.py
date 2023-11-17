from flask import Flask, render_template
import RPi.GPIO as GPIO
import sys
import sqlite3
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

R_PIN = 11  # Physical Pin 11
G_PIN = 13  # Physical Pin 13
B_PIN = 15  # Physical Pin 15

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(R_PIN, GPIO.OUT)
GPIO.setup(G_PIN, GPIO.OUT)
GPIO.setup(B_PIN, GPIO.OUT)

# Create PWM objects for each pin
RED_PWM = GPIO.PWM(R_PIN, 100)  # 100 Hz frequency
GREEN_PWM = GPIO.PWM(G_PIN, 100)
BLUE_PWM = GPIO.PWM(B_PIN, 100)

def turn_on_color(color, intensity):
    # Map intensity from the range [0, 100] to [0, 100] (adjust as needed)
    intensity = max(0, min(100, 100-int(intensity)))

    # Calculate the duty cycle based on the intensity
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

@app.route('/')
def index():
    # Retrieve data from the database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT radius, time FROM data")
    data = cursor.fetchall()
    conn.close()

    # Extract radius and time values from the database
    radii = [entry[0] for entry in data]
    times = [entry[1] for entry in data]

    # Create a plot
    plt.figure(figsize=(8, 4))
    plt.plot(times, radii, marker='o', linestyle='-', color='b')
    plt.xlabel('Time')
    plt.ylabel('Radius')
    plt.title('Radius vs. Time')
    
    # Save the plot as a PNG image in memory
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image to base64 for HTML rendering
    img_base64 = base64.b64encode(img.read()).decode()
    return render_template('home.html', image=img_base64)

@app.route("/control/<color>/<intensity>")
def control(color, intensity):
    turn_on_color(color, intensity)
    return f"Turning on {color} LED with intensity {intensity}"

if __name__ == '__main__':
    app.run(debug=True)

