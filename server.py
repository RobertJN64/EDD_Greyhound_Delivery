from tools.object_map import ObjectMap
from hardware.robot import Robot
import flask

app = flask.Flask(__name__)
robot = Robot()

@app.route('/')
def home():
    return "OK"

#region CONTROL PAGE
robot_om = ObjectMap(robot)

py_control_content = robot_om.generate_html('Robot')
@app.route('/py_control')
def py_control():
    return flask.render_template('py_control.html', content=py_control_content)
#endregion

def startFlask():
    app.run(host="0.0.0.0", port=80)

startFlask()