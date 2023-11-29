import threading
import time
import cv2


class Camera:
    def __init__(self):
        self._cap = cv2.VideoCapture(0)
        #threading.Thread(target=self._reader, daemon=True).start()

    # grab frames as soon as they are available - this clears out the automatic buffer an ensures read is always recent
    def _reader(self):
        while True:
            self._cap.grab()
            time.sleep(0.01)

    # retrieve latest frame
    def read(self):
        t = time.time()
        self._cap.grab()
        ret, frame = self._cap.retrieve()
        print(time.time() - t)
        return frame
