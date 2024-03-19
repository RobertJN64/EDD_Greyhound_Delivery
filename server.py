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

def limit_cam_id(num_id):
    if num_id < 0 or num_id >= len(robot.vision.vpes):
        print(f"Camera id {num_id} out of range.")
        num_id = 0
    return num_id

@app.route('/camera')
def get_camera_array_fast():
    num_id = limit_cam_id(int(flask.request.args.get('id'), 0))
    w = int(flask.request.args.get('w', 800))
    h = int(flask.request.args.get('h', 640))
    img = robot.vision.vpes[num_id].camera.read(w, h)
    _, buf = cv2.imencode('.jpg', img)
    return base64.b64encode(buf)

@app.route('/tag_view')
def get_tag_view():
    num_id = limit_cam_id(int(flask.request.args.get('id'), 0))
    _, buf = cv2.imencode('.jpg', robot.vision.vpes[num_id].tag_img)
    return base64.b64encode(buf)

@app.route('/tag_data')
def get_tag_data():
    num_id = limit_cam_id(int(flask.request.args.get('id'), 0))
    return json.dumps({'ids': robot.vision.vpes[num_id].tag_ids.tolist(),
                       'tvecs': [tvec.tolist() for tvec in robot.vision.vpes[num_id].tvecs],
                       'rvecs': [rvec.tolist() for rvec in robot.vision.vpes[num_id].rvecs]})

create_WebController(robot, 'robot', app, create_private_interface=True)

def startFlask():
    app.run(host="0.0.0.0", port=80)