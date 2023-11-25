from hardware.motor_controller_emulator import MotorController_Emulator as MotorController_Emulator
from hardware.subsystem import Subsystem

class LeftMotor:
    fwd_pin = 11
    rev_pin = 8
    spd_pin = 7

class RightMotor:
    fwd_pin = 16
    rev_pin = 20
    spd_pin = 21


class DT_Emulator(Subsystem):
    def __init__(self, mc_class = MotorController_Emulator):
        self._left_motor = mc_class(LeftMotor.fwd_pin, LeftMotor.rev_pin, LeftMotor.spd_pin)
        self._right_motor = mc_class(RightMotor.fwd_pin, RightMotor.rev_pin, RightMotor.spd_pin)
        super().__init__()

    def _loop(self):
        while not self._should_kill:
            pass
        self._left_motor.stop()
        self._right_motor.stop()

    def set_speeds(self, left, right):
        self._left_motor.set_speed(left)
        self._right_motor.set_speed(right)

    def stop(self):
        self._left_motor.stop()
        self._right_motor.stop()

class DT(DT_Emulator):
    def __init__(self):
        from hardware.motor_controller import MotorController
        super().__init__(mc_class=MotorController)
