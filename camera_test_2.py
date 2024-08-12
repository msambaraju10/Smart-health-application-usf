import cv2
from flask import Flask, render_template, Response, request, jsonify


app = Flask(__name__, template_folder='./templates')

camera = cv2.VideoCapture(0)
camera.open(0, cv2.CAP_DSHOW)


def detect_face(frame):
    while camera.isOpened():
        success, frame = camera.read()
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return image

@app.route('/')
def index():
    return render_template('camera_test.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen_frames():  # generate frame by frame from camera
    global out, capture
    while True:
        success, frame = camera.read()
        if success:
                frame = detect_face(frame)
        else:
            pass

#
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', threaded=True)
