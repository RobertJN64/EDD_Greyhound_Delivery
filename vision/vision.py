from subsystem import Subsystem
from vision.camera import Camera
from time import sleep

class Vision(Subsystem):
    def __init__(self):
        self.camera = Camera()
        super().__init__()

    def _loop(self):
        while not self._should_kill:
            sleep(0.5)