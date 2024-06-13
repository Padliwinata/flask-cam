from flask import Flask, render_template, Response
import cv2

app = Flask(__name__, template_folder='templates')


def gen_frames():
    camera = cv2.VideoCapture(0)  # Capture from the default camera
    while True:
        success, frame = camera.read()  # Read the camera frame
        if not success:
            break
        else:
            # Process the frame here (e.g., convert to grayscale)
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)