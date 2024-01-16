from hardware.motor_controller_emulator import MotorController_Emulator as MotorController_Emulator
from subsystem import Subsystem
from time import sleep

class LeftFrontMotor:
    fwd_pin = 20
    rev_pin = 16
    spd_pin = 21

class RightFrontMotor:
    fwd_pin = 9
    rev_pin = 10
    spd_pin = 11

class DT_Emulator(Subsystem):
    def __init__(self, mc_class = MotorController_Emulator):
        self._left_f_motor = mc_class(LeftFrontMotor.fwd_pin, LeftFrontMotor.rev_pin, LeftFrontMotor.spd_pin)
        self._right_f_motor = mc_class(RightFrontMotor.fwd_pin, RightFrontMotor.rev_pin, RightFrontMotor.spd_pin)
        super().__init__()

    def _loop(self):
        while not self._should_kill:
            sleep(0.5)
        self.stop()

    def set_speeds(self, left, right):
        self._left_f_motor.set_speed(left)
        self._right_f_motor.set_speed(right)

    def stop(self):
        self._left_f_motor.stop()
        self._right_f_motor.stop()


class DT(DT_Emulator):
    def __init__(self):
        from hardware.motor_controller import MotorController
        super().__init__(mc_class=MotorController)
