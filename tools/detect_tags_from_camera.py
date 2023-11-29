import read_camera
import numpy as np
import render3d
import time
import epsm
import cv2

RENDER_LOOP = True

if RENDER_LOOP:
    env = render3d.create_env()

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
    mtx = np.loadtxt('calib_images/rpi/calib_mtx.calib')
    dist = np.loadtxt('calib_images/rpi/calib_dist.calib')

    t = time.time()
    while True:
        #img = vision.get_camera_image()
        img = read_camera.get_image('192.168.137.240')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        corners, ids, rejected = ad.detectMarkers(gray)
        cv2.aruco.drawDetectedMarkers(img, corners, ids)

        if len(corners) > 0:
            rvecs, tvecs, _ = epsm.estimatePoseSingleMarkers(corners, 3, mtx, dist)

            for rvec, tvec in zip(rvecs, tvecs):
                cv2.drawFrameAxes(img, mtx, dist, rvec, tvec, 1)
            if RENDER_LOOP:
                render3d.update(ids, tvecs, rvecs, env)
        else:
            if RENDER_LOOP:
                render3d.update_no_tags(env)


        cv2.imshow("Robert Ops", cv2.resize(img, (900,600)))

        cv2.waitKey(1)

        print(f"FPS: {round(1 / (time.time() - t), 2)}")
        t = time.time()



main()