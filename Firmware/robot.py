from imu import IMU_Emulator as IMU
#from imu import IMU as IMU

class Robot:
    def __init__(self):
        self.imu = IMU()

    def kill(self):
        self.imu.kill()