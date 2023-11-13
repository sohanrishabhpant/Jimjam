import numpy as np
import cv2
import matplotlib.pyplot as plt
import urllib.request
import json

WRITE_API_KEY = "P3RYOEFOD90DB9FY"
READ_API_KEY = "5Y175EF80D2KQ470"
CHANNEL_ID = "1848369"

conn = urllib.request.urlopen(
    f"http://api.thingspeak.com/update?api_key={WRITE_API_KEY}&field7=0"
)

conn.close()
