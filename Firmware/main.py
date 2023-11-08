import robot
import time
import imu


robot = robot.Robot()
imu.start_monitor_thread(robot)
while True:
    print(f"{robot.imu_angle=} {robot.imu_calib=} {robot.reset_imu=}")
    time.sleep(0.1)
