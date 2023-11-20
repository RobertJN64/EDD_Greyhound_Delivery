from drivetrain import DT_Emulator as DT
from imu import IMU_Emulator as IMU
#from drivetrain import DT as DT
#from imu import IMU as IMU

class Robot:
    def __init__(self):
        self.imu = IMU()
        self.dt = DT()

    def kill(self):
        self.imu.kill()
        self.dt.kill()