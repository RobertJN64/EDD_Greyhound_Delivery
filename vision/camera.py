import threading
import cv2

class Camera:
    def __init__(self):
        self._cap = cv2.VideoCapture(0)
        threading.Thread(target=self._reader, daemon=True).start()

    # grab frames as soon as they are available - this clears out the automatic buffer an ensures read is always recent
    def _reader(self):
        while True:
            ret = self._cap.grab()
            if not ret:
                break

    # retrieve latest frame
    def read(self):
        self._cap.grab()
        ret, frame = self._cap.retrieve()
        return frame
