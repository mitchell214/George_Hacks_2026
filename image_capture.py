import requests
import os
from datetime import datetime
import cv2
import numpy as np
import base64

SERVER_URL = "http://11.35.149.194:5050/latest.jpg"
SAVE_DIR = "camera_images"

os.makedirs(SAVE_DIR, exist_ok=True)

def fetch_image_bytes():
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

    #timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = os.path.join(SAVE_DIR, f"frame.jpg")

    cv2.imwrite(filename, frame)

    print(f"Saved image: {filename}")
    return filename

def encode_image_base64(frame):
    if frame is None:
        return None

    success, buffer = cv2.imencode(".jpg", frame)
    if not success:
        print("Failed to encode image")
        return None

    img_bytes = buffer.tobytes()
    b64_string = base64.b64encode(img_bytes).decode("utf-8")

    return b64_string

def save_base64_to_file(b64_string, filename=None):
    if not b64_string:
        return None

    if filename is None:
        #timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = os.path.join(SAVE_DIR, f"frame.txt")

    with open(filename, "w") as f:
        f.write(b64_string)

    print(f"Saved base64: {filename}")
    return filename


def capture_and_save():
    img_bytes = fetch_image_bytes()
    frame = decode_image(img_bytes)
    filename_img = save_image(frame)
    b64_string = encode_image_base64(frame)
    filename_b64 = save_base64_to_file(b64_string)
    return b64_string

if __name__ == "__main__":
    capture_and_save()