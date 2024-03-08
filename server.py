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
    num_id = int(flask.request.args.get('id'), 0)
    w = int(flask.request.args.get('w', 800))
    h = int(flask.request.args.get('h', 640))
    if num_id == 0:
        img = robot.vision.camera_0.read(w, h)
    elif num_id == 1:
        img = robot.vision.camera_1.read(w, h)
    elif num_id == 2:
        img = robot.vision.camera_2.read(w, h)
    else:
        img = robot.vision.camera_0.read(w, h)
        print("Error: id invalid")
    _, buf = cv2.imencode('.jpg', img)
    return base64.b64encode(buf)

@app.route('/tag_view')
def get_tag_view():
    num_id = int(flask.request.args.get('id'), 0)
    if num_id < 0 or num_id > 2:
        num_id = 0
    _, buf = cv2.imencode('.jpg', robot.vision.tag_img[num_id])
    return base64.b64encode(buf)

@app.route('/tag_data')
def get_tag_data():
    num_id = int(flask.request.args.get('id'), 0)
    if num_id < 0 or num_id > 2:
        num_id = 0
    return json.dumps({'ids': robot.vision.ids[num_id].tolist(),
                       'tvecs': [tvec.tolist() for tvec in robot.vision.tvecs[num_id]],
                       'rvecs': [rvec.tolist() for rvec in robot.vision.rvecs[num_id]]})

create_WebController(robot, 'robot', app, create_private_interface=True)

def startFlask():
    app.run(host="0.0.0.0", port=80)