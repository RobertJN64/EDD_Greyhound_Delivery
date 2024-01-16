EMULATE = True

if EMULATE:
    from hardware.drivetrain import DT_Emulator as DT
    from hardware.imu import IMU_Emulator as IMU
else:
    from hardware.drivetrain import DT as DT
    from hardware.imu import IMU as IMU

from vision.vision_pose_estimator import VisionPoseEstimator
from time import sleep
import threading


class Robot:
    def __init__(self):
        self.imu = IMU()
        self.dt = DT()
        self.vision = VisionPoseEstimator()

        # state machine
        self.enable_IMU_drive = False
        self.has_stopped_IMU_drive = False
        self.IMU_drive_target_speed = 0
        self.IMU_CF = 1 #correction force

        threading.Thread(target=self._IMU_drive_worker).start()

    def kill(self):
        self.imu.kill()
        self.dt.kill()
        self.vision.kill()

    def start_IMU_drive(self, speed=70):
        self.enable_IMU_drive = True
        self.IMU_drive_target_speed = speed

    def stop_IMU_drive(self):
        self.enable_IMU_drive = False

    def _IMU_drive_worker(self):
        while True:
            if self.enable_IMU_drive:
                self.imu._reset() #do non-async reset
                while self.enable_IMU_drive:
                    left = self.IMU_drive_target_speed + self.imu.angle * self.IMU_CF
                    right = self.IMU_drive_target_speed - self.imu.angle * self.IMU_CF

                    self.dt.set_speeds(left, right)
                    sleep(0.05)
                self.dt.stop()
            sleep(0.1)

    def set_IMU_CF(self, value=1):
        self.IMU_CF = value