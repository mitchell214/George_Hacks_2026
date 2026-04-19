from flask import Flask, Response, request, jsonify
from picamera2 import Picamera2
import threading
import time
from flask_cors import CORS
import cv2

app = Flask(__name__)
CORS(app)

picam2 = Picamera2()

config = picam2.create_video_configuration(
    main={"format": "RGB888", "size": (640, 480)}
)

picam2.configure(config)
picam2.start()

time.sleep(1)

latest_frame = None
latest_lock = threading.Lock()

def capture_loop():
    global latest_frame

    while True:
        frame = picam2.capture_array()

        # rotate 90° left
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        success, jpeg = cv2.imencode(".jpg", frame)

        if success:
            new_frame = jpeg.tobytes()

            # fast atomic swap
            with latest_lock:
                latest_frame = new_frame

        time.sleep(0.1)

threading.Thread(target=capture_loop, daemon=True).start()

@app.route("/latest.jpg", methods=["GET"])
def latest():
    with latest_lock:
        frame = latest_frame

    if frame is None:
        return "No frame yet", 503

    return Response(frame, mimetype="image/jpeg")

@app.route("/stream.mjpg", methods=["GET"])
def stream():
    def generate():
        while True:
            with latest_lock:
                frame = latest_frame

            if frame:
                yield (
                    b"--frame\r\n"
                    b"Content-Type: image/jpeg\r\n\r\n" +
                    frame +
                    b"\r\n"
                )

            time.sleep(0.05)

    return Response(
        generate(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/control", methods=["POST"])
def control():
    data = request.get_json(silent=True) or {}
    cmd = data.get("command")

    if cmd == "restart_camera":
        picam2.stop()
        picam2.start()
        return jsonify({"status": "camera restarted"})

    if cmd == "status":
        return jsonify({"status": "running"})

    return jsonify({"error": "unknown command"}), 400

@app.route("/api/<path:endpoint>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def api_gateway(endpoint):

    data = request.get_json(silent=True)

    if endpoint == "frame" and request.method == "GET":
        with latest_lock:
            if latest_frame is None:
                return jsonify({"error": "no frame"}), 503

            import base64
            b64 = base64.b64encode(latest_frame).decode("utf-8")

        return jsonify({"image_base64": b64})

    if endpoint == "message" and request.method == "POST":
        prompt = (data or {}).get("prompt", "")

        return jsonify({
            "received": prompt,
            "status": "ok"
        })

    if endpoint == "camera" and request.method == "POST":
        cmd = (data or {}).get("command")

        if cmd == "restart":
            picam2.stop()
            picam2.start()
            return jsonify({"status": "restarted"})

        return jsonify({"error": "unknown command"}), 400

    return jsonify({
        "endpoint": endpoint,
        "method": request.method,
        "data": data,
        "status": "unhandled route"
    })

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