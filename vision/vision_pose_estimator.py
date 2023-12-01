from subsystem import Subsystem
from vision.camera import Camera
import numpy as np
import cv2

def estimatePoseSingleMarkers(corners, marker_size, mtx, distortion):
    """
    This will estimate the rvec and tvec for each of the marker corners detected by:
       corners, ids, rejectedImgPoints = detector.detectMarkers(image)
    corners - is an array of detected corners for each detected marker in the image
    marker_size - is the size of the detected markers
    mtx - is the camera matrix
    distortion - is the camera distortion matrix
    RETURN list of rvecs, tvecs, and trash (so that it corresponds to the old estimatePoseSingleMarkers())
    """
    marker_points = np.array([[-marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, -marker_size / 2, 0],
                              [-marker_size / 2, -marker_size / 2, 0]], dtype=np.float32)
    trash = []
    rvecs = []
    tvecs = []
    for c in corners:
        nada, R, t = cv2.solvePnP(marker_points, c, mtx, distortion, False, cv2.SOLVEPNP_IPPE_SQUARE)
        rvecs.append(R)
        tvecs.append(t)
        trash.append(nada)
    return rvecs, tvecs, trash

def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

dp = cv2.aruco.DetectorParameters()
arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
ad = cv2.aruco.ArucoDetector(arucoDict, dp)

class VisionPoseEstimator(Subsystem):
    def __init__(self, enable_image_vis = True):
        self.camera = Camera()
        self.enable_image_vis = enable_image_vis
        self._mtx = np.loadtxt('vision/calib_mtx.calib')
        self._dist = np.loadtxt('vision/calib_dist.calib')
        self.tag_img = None
        super().__init__()

    def _loop(self):
        while not self._should_kill:
            img = self.camera.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            corners, ids, rejected = ad.detectMarkers(gray)
            cv2.aruco.drawDetectedMarkers(img, corners, ids)

            if len(corners) > 0:
                rvecs, tvecs, _ = estimatePoseSingleMarkers(corners, 3, self._mtx, self._dist)

                if self.enable_image_vis:
                    for rvec, tvec in zip(rvecs, tvecs):
                        cv2.drawFrameAxes(img, self._mtx, self._dist, rvec, tvec, 1)
                        self.tag_img = img.copy()

                    #render3d.update(ids, tvecs, rvecs, env)
            else:
                if self.enable_image_vis:
                    self.tag_img = img.copy()
            #     render3d.update_no_tags(env)