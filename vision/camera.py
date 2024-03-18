import threading
import time
import cv2

class Camera:
    def __init__(self, num_id: int = 0):
        self._cap = cv2.VideoCapture(num_id)
        self._cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self._cap.grab()
        ret, frame = self._cap.retrieve()
        assert ret, "Creating camera failed"

        #threading.Thread(target=self._reader, daemon=True).start()

    # grab frames as soon as they are available - this clears out the automatic buffer an ensures read is always recent
    def _reader(self):
        while True:
            self._cap.grab()
            time.sleep(0.01)

    # retrieve latest frame
    def read(self, w=800, h=640):
        self._cap.grab()
        ret, frame = self._cap.retrieve()
        return cv2.convertScaleAbs(cv2.resize(frame, (w,h)), alpha=1.5, beta=0.5)
