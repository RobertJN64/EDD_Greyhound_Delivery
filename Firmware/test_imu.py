import robot
import time

robot = robot.Robot()
while True:
    print(f"{robot.imu.angle=} {robot.imu.should_calibrate=} {robot.imu.should_reset=}")
    k = input("[r]eset / [c]alibrate / [k]ill")
    robot.imu.should_reset = (robot.imu.should_reset or k == 'r')
    robot.imu.should_calibrate = (robot.imu.should_calibrate or k == 'c')
    if k == 'k':
        robot.kill()
        break
    time.sleep(0.1)
