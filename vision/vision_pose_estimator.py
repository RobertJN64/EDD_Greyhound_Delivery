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

dp = cv2.aruco.DetectorParameters()
arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
ad = cv2.aruco.ArucoDetector(arucoDict, dp)

class MultiCamEstimator(Subsystem):
    def __init__(self, cam_srcs: list[int], flips: list[bool], enable_image_vis:bool = True):
        self.vpes = []

        for cam_id, (cam_src, flip) in enumerate(zip(cam_srcs, flips)):
            vpe = VisionPoseEstimator(cam_id, cam_src, flip, enable_image_vis)

            self.vpes.append(vpe)

        print(f"Created {len(self.vpes)} Cameras!")
        super().__init__()

    def _loop(self):
        while not self._should_kill:
            for vpe in self.vpes:
                vpe.update_tag_pos()

            #TODO - pose fuse


class VisionPoseEstimator:
    def __init__(self, cam_id, cam_src, flip, enable_image_vis):
        self.camera = Camera(cam_src)
        self.enable_image_vis = enable_image_vis
        self._mtx = np.loadtxt(f'vision/{cam_id}/calib_mtx.calib') #TODO - complete this calibration
        self._dist = np.loadtxt(f'vision/{cam_id}/calib_dist.calib')
        self.tag_img = None

        self.tag_ids = np.empty(0)
        self.rvecs = []
        self.tvecs = []

        self.flip = flip

        super().__init__()

    def update_tag_pos(self):
        img = self.camera.read()

        if self.flip:
            img = cv2.flip(img, 0)
            img = cv2.flip(img, 1)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        corners, ids, rejected = ad.detectMarkers(gray)
        cv2.aruco.drawDetectedMarkers(img, corners, ids)

        if len(corners) > 0:
            rvecs, tvecs, _ = estimatePoseSingleMarkers(corners, 3, self._mtx, self._dist)

            self.tag_ids = ids
            self.rvecs = rvecs
            self.tvecs = tvecs

            if self.enable_image_vis:
                for rvec, tvec in zip(rvecs, tvecs):
                    cv2.drawFrameAxes(img, self._mtx, self._dist, rvec, tvec, 1)
                    self.tag_img = img.copy()

        else:
            if self.enable_image_vis:
                self.tag_img = img.copy()

            self.tag_ids = np.empty(0)
            self.rvecs = []
            self.tvecs = []
