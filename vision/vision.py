from subsystem import Subsystem
from vision.camera import Camera

class Vision(Subsystem):
    def __init__(self):
        self.camera = Camera()
        super().__init__()

    def _loop(self):
        while not self._should_kill:
            pass