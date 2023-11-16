import threading

class B_VideoCapture:
    def __init__(self, name):
        self.cap = cv2.VideoCapture(name)
        #self.t = threading.Thread(target=self._reader)
        #self.t.daemon = True
        #self.t.start()

    # grab frames as soon as they are available
    def _reader(self):
        while True:
            ret = self.cap.grab()
            if not ret:
                break

    # retrieve latest frame
    def read(self):
        self.cap.grab()
        ret, frame = self.cap.retrieve()
        return frame

import cv2
cam = B_VideoCapture(0)
img = cam.read()
cv2.imwrite('sample.jpg', img) 

