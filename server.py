from tools.web_object_map import create_WebObjectMap_server
from hardware.robot import Robot
import flask

app = flask.Flask(__name__)
robot = Robot()

@app.route('/')
def home():
    return "OK"

create_WebObjectMap_server(app, 'Robot', robot)

def startFlask():
    app.run(host="0.0.0.0", port=80)

startFlask()