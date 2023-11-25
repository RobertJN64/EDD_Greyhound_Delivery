EMULATE = True

if EMULATE:
    from hardware.drivetrain import DT_Emulator as DT
    from hardware.imu import IMU_Emulator as IMU
else:
    from hardware.drivetrain import DT as DT
    from hardware.imu import IMU as IMU

class Robot:
    def __init__(self):
        self.imu = IMU()
        self.dt = DT()

    def kill(self):
        self.imu.kill()
        self.dt.kill()