import requests
import os
from datetime import datetime
import cv2
import numpy as np

SERVER_URL = "http://11.35.149.194:5050/latest.jpg"
SAVE_DIR = "camera_images"

os.makedirs(SAVE_DIR, exist_ok=True)

def fetch_image_bytes():
    """
    Downloads latest image from server.
    Returns raw image bytes or None.
    """

    try:
        response = requests.get(SERVER_URL, timeout=5)

        if response.status_code != 200:
            print(f"HTTP error: {response.status_code}")
            return None

        return response.content

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None

def decode_image(image_bytes):
    if not image_bytes:
        return None

    arr = np.frombuffer(image_bytes, dtype=np.uint8)
    frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)

    if frame is None:
        print("Failed to decode image")
        return None

    return frame

def save_image(frame):
    if frame is None:
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = os.path.join(SAVE_DIR, f"frame_{timestamp}.jpg")

    cv2.imwrite(filename, frame)

    print(f"Saved: {filename}")
    return filename


def capture_and_save():
    """
    Fetches image from Pi server and saves it locally.
    """

    img_bytes = fetch_image_bytes()
    frame = decode_image(img_bytes)
    return save_image(frame)

if __name__ == "__main__":
    capture_and_save()