class MotorController_Emulator:
    def __init__(self, fwdPin: int, revPin: int, spdPin: int):
        self.fwdPin = fwdPin
        self.revPin = revPin
        self.spdPin = spdPin

    def setup(self):
        pass

    def forward(self, speed):
        print(f"Running motors forward at {speed=}")

    def backward(self, speed):
        print(f"Running motors backward at {speed=}")

    def stop(self):
        print("Stopping motors")


    def set_speed(self, speed):
        if speed == 0:
            self.stop()
        elif speed > 0:
            self.forward(abs(speed))
        else:
            self.backward(abs(speed))