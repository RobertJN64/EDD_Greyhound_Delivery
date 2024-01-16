class MotorController_Emulator:
    def __init__(self, fwdPin: int, revPin: int, spdPin: int):
        self.fwdPin = fwdPin
        self.revPin = revPin
        self.spdPin = spdPin

    def forward(self, speed):
        print(f"Running motor forward at {speed=}")

    def backward(self, speed):
        print(f"Running motor backward at {speed=}")

    def stop(self):
        print("Stopping motor")


    def set_speed(self, speed):
        if speed == 0:
            self.stop()
        elif speed > 0:
            self.forward(min(abs(speed), 100))
        else:
            self.backward(min(abs(speed), 100))