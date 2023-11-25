from flask import request
from hardware.robot import Robot
import flask
import json

app = flask.Flask(__name__)
robot = Robot()

btn_func_map = []
def register_function(name, f, args=None):
    btn_func_map.append((name, f, args))
register_function('robot.kill', robot.kill)
register_function('robot.imu.calibrate', robot.imu.calibrate)
register_function('robot.imu.reset', robot.imu.reset)
register_function('robot.dt.stop', robot.dt.stop)
register_function('robot.dt.set_speeds', robot.dt.set_speeds, ['left', 'right'])

@app.route('/')
def home():
    return "OK"

@app.route('/get_vars')
def get_vars():
    payload = [
        ('robot.imu.angle', robot.imu.angle),
        ('robot.imu.should_reset', robot.imu.should_reset),
        ('robot.imu.should_calibrate', robot.imu.should_calibrate),
        ('robot.imu.should_kill', robot.imu.should_kill)
    ]
    return json.dumps(payload)

@app.route('/get_quick_actions')
def get_quick_actions():
    return json.dumps([name for name, f in btn_func_map])


@app.route('/quick_action/<action>')
def quick_action(action):
    for name, f, args in btn_func_map:
        if name == action:
            if args is None:
                args = []
            for arg in args:
                if arg not in request.args:
                    return f"Missing {arg=}"
            for arg in request.args:
                if arg not in args:
                    return f"Extra {arg=}"

            f(**{name: int(arg) for name, arg in request.args.items()})
            break
    else:
        return "Function name not found"
    return "OK"

def startFlask():
    app.run(host="0.0.0.0", port=80)