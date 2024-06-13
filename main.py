from flask import Flask, render_template, request, jsonify
import cv2
import numpy as np
import base64

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_frame', methods=['POST'])
def process_frame():
    data = request.json
    img_data = data['image']
    img_data = img_data.split(",")[1]
    img_bytes = base64.b64decode(img_data)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Process the frame (e.g., convert to grayscale)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Convert the processed frame back to base64 to send back to the client
    _, buffer = cv2.imencode('.jpg', gray)
    processed_img = base64.b64encode(buffer).decode('utf-8')

    return jsonify({'image': 'data:image/jpeg;base64,' + processed_img})


if __name__ == '__main__':
    app.run(debug=True)
