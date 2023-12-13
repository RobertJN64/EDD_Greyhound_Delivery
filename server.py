from PyObjectInterface.WebController import create_WebController
from robot import Robot
import base64
import flask
import json
import cv2

app = flask.Flask(__name__)
robot = Robot()

@app.route('/')
def home():
    return "OK"

@app.route('/camera')
def get_camera_array_fast():
    w = int(flask.request.args.get('w', 800))
    h = int(flask.request.args.get('h', 640))
    img = robot.vision.camera.read(w, h)
    _, buf = cv2.imencode('.jpg', img)
    return base64.b64encode(buf)

@app.route('/tag_view')
def get_tag_view():
    _, buf = cv2.imencode('.jpg', robot.vision.tag_img)
    return base64.b64encode(buf)

@app.route('/tag_data')
def get_tag_data():
    return json.dumps({'ids': robot.vision.ids,
                       'tvecs': robot.vision.tvecs.tolist(),
                       'rvecs': robot.vision.rvecs.tolist()})

# create_WebController(robot, 'robot', app, create_private_interface=False)

def startFlask():
    app.run(host="0.0.0.0", port=80)