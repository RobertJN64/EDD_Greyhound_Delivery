from motor_controller_emulator import MotorController_Emulator
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

class MotorController(MotorController_Emulator):
    def __init__(self, fwdPin: int, revPin: int, spdPin: int):
        super().__init__(fwdPin, revPin, spdPin)
        GPIO.setup(self.fwdPin, GPIO.OUT)
        GPIO.setup(self.revPin, GPIO.OUT)
        GPIO.setup(self.spdPin, GPIO.OUT)

        GPIO.output(self.fwdPin, GPIO.LOW)
        GPIO.output(self.revPin, GPIO.LOW)

        self.pwm = GPIO.PWM(spdPin, 1000)  # 1000 is freq
        self.pwm.start(0)

    def forward(self, speed):
        GPIO.output(self.revPin, GPIO.LOW)
        GPIO.output(self.fwdPin, GPIO.HIGH)
        self.pwm.ChangeDutyCycle(abs(speed))

    def backward(self, speed):
        GPIO.output(self.fwdPin, GPIO.LOW)
        GPIO.output(self.revPin, GPIO.HIGH)
        self.pwm.ChangeDutyCycle(abs(speed))

    def stop(self):
        GPIO.output(self.fwdPin, GPIO.LOW)
        GPIO.output(self.revPin, GPIO.LOW)
        self.pwm.ChangeDutyCycle(0)