import cv_robot.vision as vision
import numpy as np
import time
import cv2
vision.activate_camera()

dp = cv2.aruco.DetectorParameters()
arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
ad = cv2.aruco.ArucoDetector(arucoDict, dp)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)

def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)
    return img

def main():
    mtx = np.loadtxt('calib_images/laptop/calib_mtx.calib')
    dist = np.loadtxt('calib_images/laptop/calib_dist.calib')


    t = time.time()
    while True:
        img = vision.get_camera_image()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (5,5), None)
        #corners, ids, rejected = ad.detectMarkers(img)
        #cv2.aruco.drawDetectedMarkers(img, corners, ids)
        #cv2.aruco.drawDetectedMarkers(img, rejected)

        print(corners)

        if ret:
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            # Find the rotation and translation vectors.
            ret, rvecs, tvecs = cv2.solvePnP(objp, corners2, mtx, dist)
            # project 3D points to image plane
            imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
            img = draw(img, corners2, imgpts)

        cv2.imshow("Robert Ops", img)

        cv2.waitKey(1)

        print(f"FPS: {round(1 / (time.time() - t), 2)}")
        t = time.time()

main()