from subsystem import Subsystem
import time

scale_f = 0.8

# some MPU6050 Registers and their Address
class MPU6050:
    Device_Address = 0x68  # MPU6050 device address

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

class IMU_Emulator(Subsystem):
    def __init__(self):
        self.angle = 0
        self._gyrototal = 0 #internal angle rep
        self._drift = 0
        self._should_calibrate = True
        self._should_reset = False
        self._reset_target_angle = 0
        super().__init__()

    def calibrate(self):
        """Trigger an async calibration"""
        self._should_calibrate = True

    def reset(self, set_angle_to=0):
        """Trigger an async reset"""
        self._reset_target_angle = set_angle_to
        self._should_reset = True

    def _calibrate(self):
        """Internal calibration function - to trigger a calibrate call .calibrate()"""
        self._reset_target_angle = 0
        self._reset()
        time.sleep(5)
        self._should_calibrate = False

    def _reset(self):
        """Internal reset function - to trigger a reset call .reset()"""
        self._gyrototal = 0
        self.angle = self._reset_target_angle
        self._should_reset = False

    def _read(self):
        self.angle += 1
        self.angle = self.angle % 360
        time.sleep(0.5)

    def _loop(self):
        while not self._should_kill:
            print("Calibrating IMU...")
            self._calibrate()
            while not (self._should_kill or self._should_calibrate):
                self._read()
                if self._should_reset:
                    print("Reset IMU angle...")
                    self._reset()

    def heading(self):
        """returns angle -180 to 180"""
        if self.angle > 180:
            return self.angle - 360
        return self.angle

class IMU(IMU_Emulator):
    def __init__(self):
        import smbus
        self._bus = smbus.SMBus(1)  # or bus = smbus.SMBus(0) for older version boards
        # write to sample rate register
        self._bus.write_byte_data(MPU6050.Device_Address, MPU6050.SMPLRT_DIV, 7)
        # Write to power management register
        self._bus.write_byte_data(MPU6050.Device_Address, MPU6050.PWR_MGMT_1, 1)
        # Write to Configuration register
        self._bus.write_byte_data(MPU6050.Device_Address, MPU6050.CONFIG, 0)
        # Write to Gyro configuration register
        self._bus.write_byte_data(MPU6050.Device_Address, MPU6050.GYRO_CONFIG, 24)
        # Write to interrupt enable register
        self._bus.write_byte_data(MPU6050.Device_Address, MPU6050.INT_ENABLE, 1)
        super().__init__()

    def _read_raw_data(self, addr):
        # Accelero and Gyro value are 16-bit
        high = self._bus.read_byte_data(MPU6050.Device_Address, addr)
        low = self._bus.read_byte_data(MPU6050.Device_Address, addr + 1)

        # concatenate higher and lower value
        value = ((high << 8) | low)

        # to get signed value from mpu6050
        if value > 32768:
            value -= 65536
        return value

    def _calibrate(self):
        """Internal calibration function - to trigger a calibrate call .calibrate()"""
        self._reset_target_angle = 0
        self._reset()
        self._drift = 0
        for i in range(0, 100):
            t = time.time()
            gyro_z = self._read_raw_data(MPU6050.GYRO_ZOUT_H)
            # Full scale range +/- 250 degree/C as per sensitivity scale factor
            Gz = (gyro_z / 131.0) * scale_f
            self._drift += Gz
            time.sleep(0.05 - (time.time() - t))

        self._drift /= 100
        self._should_calibrate = False

    def _read(self):
        t = time.time()
        gyro_z = self._read_raw_data(MPU6050.GYRO_ZOUT_H)
        # Full scale range +/- 250 degree/C as per sensitivity scale factor
        Gz = (gyro_z / 131.0) * scale_f
        self._gyrototal -= (Gz - self._drift) / 2
        self.angle = round(self._gyrototal, 3) % 360
        time.sleep(0.05 - (time.time() - t))