import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO  # Import the GPIO library

# GPIO setup
GPIO.setmode(GPIO.BCM)
RED_LED_PIN = 17  # Replace with the actual GPIO pin for the red LED
GREEN_LED_PIN = 18  # Replace with the actual GPIO pin for the green LED
BLUE_LED_PIN = 27  # Replace with the actual GPIO pin for the blue LED
GPIO.setup(RED_LED_PIN, GPIO.OUT)
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)
GPIO.setup(BLUE_LED_PIN, GPIO.OUT)

# Create a VideoCapture object
cap = cv2.VideoCapture(0)
print("started")

# Define the codec and create a VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

# Initialize the arrays to store data
times = {
    'red': [],
    'green': [],
    'blue': [],
}
radii = {
    'red': [],
    'green': [],
    'blue': [],
}

# Define LED control parameters
LED_COLORS = [RED_LED_PIN, GREEN_LED_PIN, BLUE_LED_PIN]
LED_NAMES = ['red', 'green', 'blue']
LED_DURATIONS = [5, 5, 5]  # Seconds for each LED color
LED_INDEX = 0

# Capture the video for 15 seconds and store the frames in an array
frames = []
start_time = time.time()

while time.time() - start_time < sum(LED_DURATIONS):
    ret, frame = cap.read()
    frames.append(frame)

# Release the resources
cap.release()

# Process the frames and store the radii in an array
for i in range(len(frames)):
    frame = frames[i]

    if time.time() - start_time > sum(LED_DURATIONS[:LED_INDEX]):
        # Switch to the next LED color
        LED_INDEX += 1

    # Control LEDs based on LED_INDEX
    GPIO.output(RED_LED_PIN, GPIO.LOW)
    GPIO.output(GREEN_LED_PIN, GPIO.LOW)
    GPIO.output(BLUE_LED_PIN, GPIO.LOW)

    if LED_INDEX < len(LED_COLORS):
        GPIO.output(LED_COLORS[LED_INDEX], GPIO.HIGH)

    # Convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Detect the eye region using a cascade classifier
    eye_cascade = cv2.CascadeClassifier('./haarcascade_eye.xml')
    eyes = eye_cascade.detectMultiScale(gray_blur, 1.3, 5)

    if len(eyes) == 0:
        continue

    # Get the eye region and calculate the radius of the pupil
    for (ex, ey, ew, eh) in eyes:
        eye_roi = gray_blur[ey:ey+eh, ex:ex+ew]

        # Apply thresholding to separate the pupil from the iris
        _, threshold = cv2.threshold(eye_roi, 40, 255, cv2.THRESH_BINARY_INV)

        # Find the contours of the thresholded image
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Find the contour with the largest area, which corresponds to the pupil
        if len(contours) > 0:
            pupil_contour = max(contours, key=cv2.contourArea)

            # Calculate the radius of the pupil
            radius = int(cv2.minEnclosingCircle(pupil_contour)[1])

            # Append the current time and radius to the arrays
            current_time = time.time() - start_time
            times[LED_NAMES[LED_INDEX]].append(current_time)
            radii[LED_NAMES[LED_INDEX]].append(radius)

            # Draw the circle around the pupil on the original image
            cv2.circle(frame, (ex+int(pupil_contour[:, 0, 0].mean()), ey+int(pupil_contour[:, 0, 1].mean())), radius, (0, 255, 0), 2)

    # Write the frame to the output video
    out.write(frame)

# Release the video writer
out.release()

# Cleanup GPIO
GPIO.cleanup()

# Create separate graphs for each LED color
for led_color in LED_NAMES:
    plt.plot(times[led_color], radii[led_color])
    plt.xlabel('Time (s)')
    plt.ylabel('Radius')
    plt.title(f'Pupil Radius over Time (Color: {led_color.capitalize()})')
    plt.show()
