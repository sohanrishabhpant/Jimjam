from flask import Flask, render_template
import sqlite3
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)

