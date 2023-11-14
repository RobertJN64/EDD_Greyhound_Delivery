from subsystem import Subsystem
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

class IMU_Emulator(Subsystem):
    def __init__(self):
        self.angle = 0
        self.gyrototal = 0 #internal angle rep
        self.drift = 0
        self.should_calibrate = True
        self.should_reset = False
        super().__init__()

    def setup(self):
        pass

    def calibrate(self):
        """Trigger an async calibration"""
        self.should_calibrate = True

    def reset(self):
        """Trigger an async reset"""
        self.should_reset = True

    def _calibrate(self):
        """Internal calibration function - to trigger a calibrate call .calibrate()"""
        self._reset()
        time.sleep(5)
        self.should_calibrate = False

    def _reset(self):
        """Internal reset function - to trigger a reset call .reset()"""
        self.gyrototal = 0
        self.angle = 0
        self.should_reset = False

    def read(self):
        self.angle += 1
        self.angle = self.angle % 360
        time.sleep(0.5)

    def loop(self):
        while not self.should_kill:
            print("Calibrating IMU...")
            self._calibrate()
            while not (self.should_kill or self.should_calibrate):
                self.read()
                if self.should_reset:
                    print("Reset IMU angle...")
                    self._reset()

class IMU(IMU_Emulator):
    def __init__(self):
        import smbus
        self.bus = smbus.SMBus(1)  # or bus = smbus.SMBus(0) for older version boards
        self.Device_Address = 0x68  # MPU6050 device address
        super().__init__()

    def setup(self):
        """Setup I2C bus for IMU"""
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

    def _calibrate(self):
        """Internal calibration function - to trigger a calibrate call .calibrate()"""
        self._reset()
        self.drift = 0
        for i in range(0, 100):
            t = time.time()
            gyro_z = self.read_raw_data(GYRO_ZOUT_H)
            # Full scale range +/- 250 degree/C as per sensitivity scale factor
            Gz = (gyro_z / 131.0) * scale_f
            self.drift += Gz
            time.sleep(0.05 - (time.time() - t))

        self.drift /= 100
        self.should_calibrate = False

    def read(self):
        t = time.time()
        gyro_z = self.read_raw_data(GYRO_ZOUT_H)
        # Full scale range +/- 250 degree/C as per sensitivity scale factor
        Gz = (gyro_z / 131.0) * scale_f
        self.gyrototal -= (Gz - self.drift) / 2
        self.angle = round(self.gyrototal, 3) % 360
        time.sleep(0.05 - (time.time() - t))