from PyObjectInterface.WebController import create_WebController
from hardware.robot import Robot
import flask

app = flask.Flask(__name__)
robot = Robot()

@app.route('/')
def home():
    return "OK"

create_WebController(robot, 'robot', app)

def startFlask():
    app.run(host="0.0.0.0", port=80)

startFlask()