import threading
import flask
import base64

app = flask.Flask(__name__)
class B_VideoCapture:
    def __init__(self, name):
        self.cap = cv2.VideoCapture(name)
        self.t = threading.Thread(target=self._reader)
        self.t.daemon = True
        self.t.start()

    # grab frames as soon as they are available
    def _reader(self):
        while True:
            ret = self.cap.grab()
            if not ret:
                break

    # retrieve latest frame
    def read(self):
        self.cap.grab()
        ret, frame = self.cap.retrieve()
        return frame

app = flask.Flask(__name__)
import cv2
cam = B_VideoCapture(0)


@app.route('/')
def home():
    return "OK"

@app.route('/camera')
def get_camera_array_fast():
    img = cam.read()
#    img = cv2.resize(img, (320,320))
    _, buf = cv2.imencode('.jpg', img)
    return base64.b64encode(buf)


app.run(host="0.0.0.0", port=80)
