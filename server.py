from PyObjectInterface.WebController import create_WebController
from robot import Robot
import base64
import flask
import cv2

app = flask.Flask(__name__)
robot = Robot()

@app.route('/')
def home():
    return "OK"

@app.route('/camera')
def get_camera_array_fast():
    img = robot.vision.camera.read()
    w = int(flask.request.args.get('w'))
    h = int(flask.request.args.get('h'))
    img = cv2.resize(img, (w,h))
    _, buf = cv2.imencode('.jpg', img)
    return base64.b64encode(buf)

@app.route('/camera_full')
def get_camera_array_full():
    img = robot.vision.camera.read()
    _, buf = cv2.imencode('.jpg', img)
    return base64.b64encode(buf)


create_WebController(robot, 'robot', app, create_private_interface=False)

def startFlask():
    app.run(host="0.0.0.0", port=80)