from robot import Robot
import threading
import time

scale_f = 0.8

# some MPU6050 Registers and their Address
PWR_MGMT_1 = 0x6B
SMPLRT_DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_ENABLE = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

class IMU:
    def __init__(self, robot: Robot):
        import smbus
        self.robot = robot
        self.bus = smbus.SMBus(1)  # or bus = smbus.SMBus(0) for older version boards
        self.Device_Address = 0x68  # MPU6050 device address

    def init(self):
        # write to sample rate register
        self.bus.write_byte_data(self.Device_Address, SMPLRT_DIV, 7)

        # Write to power management register
        self.bus.write_byte_data(self.Device_Address, PWR_MGMT_1, 1)

        # Write to Configuration register
        self.bus.write_byte_data(self.Device_Address, CONFIG, 0)

        # Write to Gyro configuration register
        self.bus.write_byte_data(self.Device_Address, GYRO_CONFIG, 24)

        # Write to interrupt enable register
        self.bus.write_byte_data(self.Device_Address, INT_ENABLE, 1)

    def read_raw_data(self, addr):
        # Accelero and Gyro value are 16-bit
        high = self.bus.read_byte_data(self.Device_Address, addr)
        low = self.bus.read_byte_data(self.Device_Address, addr + 1)

        # concatenate higher and lower value
        value = ((high << 8) | low)

        # to get signed value from mpu6050
        if value > 32768:
            value -= 65536
        return value

    def read(self):
        while True:
            self.robot.imu_calib = True
            gyrototal = 0
            print("CALIBRATING...")
            drift = 0

            for i in range(0, 100):
                t = time.time()
                gyro_z = self.read_raw_data(GYRO_ZOUT_H)
                # Full scale range +/- 250 degree/C as per sensitivity scale factor
                Gz = (gyro_z / 131.0) * scale_f
                drift += Gz
                time.sleep(0.05 - (time.time() - t))

            drift /= 100
            self.robot.imu_calib = False

            while not self.robot.imu_calib:
                t = time.time()
                gyro_z = self.read_raw_data(GYRO_ZOUT_H)
                # Full scale range +/- 250 degree/C as per sensitivity scale factor
                Gz = (gyro_z / 131.0) * scale_f
                gyrototal -= (Gz - drift)/2
                self.robot.imu_angle = round(gyrototal, 3) % 360
                time.sleep(0.05 - (time.time() - t))
            
                if self.robot.reset_imu:
                    gyrototal = 0
                    self.robot.imu_angle = 0
                    self.robot.reset_imu = False

                if self.robot.kill:
                    break
            if self.robot.kill:
                break

class IMU_Emulator:
    def __init__(self, robot: Robot):
        self.robot = robot

    def init(self):
        pass

    def read(self):
        while True:
            self.robot.imu_calib = True
            time.sleep(5)
            self.robot.imu_calib = False
            self.robot.imu_angle = 0

            while not self.robot.imu_calib:
                self.robot.imu_angle += 10
                self.robot.imu_angle = self.robot.imu_angle%360
                time.sleep(5)
                if self.robot.reset_imu:
                    self.robot.imu_angle = 0
                    self.robot.reset_imu = False
                if self.robot.kill:
                    break
            if self.robot.kill:
                break


def IMU_worker(robot):
    imu = IMU(robot)
    #imu = IMU_Emulator(robot)
    imu.init()
    imu.read()


def start_monitor_thread(robot):
    threading.Thread(target=IMU_worker, args=[robot]).start()