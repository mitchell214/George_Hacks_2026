from flask import Flask, Response
from picamera2 import Picamera2
import threading
import time

app = Flask(__name__)

picam2 = Picamera2()

config = picam2.create_video_configuration(
    main={"format": "RGB888", "size": (640, 480)}
)

picam2.configure(config)
picam2.start()

time.sleep(1)

latest_frame = None
lock = threading.Lock()

def capture_loop():
    global latest_frame

    while True:
        frame = picam2.capture_array()

        import cv2
        success, jpeg = cv2.imencode(".jpg", frame)

        if success:
            with lock:
                latest_frame = jpeg.tobytes()

        time.sleep(0.1)


threading.Thread(target=capture_loop, daemon=True).start()

@app.route("/latest.jpg")
def latest():
    with lock:
        if latest_frame is None:
            return "No frame yet", 503

        return Response(latest_frame, mimetype="image/jpeg")

@app.route("/stream.mjpg")
def stream():
    def generate():
        while True:
            with lock:
                frame = latest_frame

            if frame:
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" +
                    frame +
                    b"\r\n"
                )

            time.sleep(0.1)

    return Response(
        generate(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/")
def index():
    return """
    <html>
    <head>
        <title>Pi Camera Server</title>
        <style>
            body { background:#111; color:white; text-align:center; font-family:Arial; }
            img { width:80%; max-width:900px; border-radius:10px; border:2px solid #444; }
        </style>
    </head>
    <body>
        <h1>Live Camera Feed</h1>

        <!-- Recommended: MJPEG stream -->
        <img src="/stream.mjpg">

    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5050,
        threaded=True,
        debug=False
    )
