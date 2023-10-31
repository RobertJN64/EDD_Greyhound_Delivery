import cv_robot.vision as vision
import time
import cv2
vision.activate_camera()

dp = cv2.aruco.DetectorParameters()
arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_250)
ad = cv2.aruco.ArucoDetector(arucoDict, dp)


t = time.time()
while True:
    img = vision.get_camera_image()
    corners, ids, rejected = ad.detectMarkers(img)
    cv2.aruco.drawDetectedMarkers(img, corners, ids)
    #cv2.aruco.drawDetectedMarkers(img, rejected)

    cv2.imshow("Robert Ops", img)

    cv2.waitKey(1)

    print(f"FPS: {round(1 / (time.time() - t), 2)}")
    t = time.time()



# cv::Mat cameraMatrix, distCoeffs;
# // You can read camera parameters from tutorial_camera_params.yml
# readCameraParameters(cameraParamsFilename, cameraMatrix, distCoeffs); // This function is implemented in aruco_samples_utility.hpp
# std::vector<cv::Vec3d> rvecs, tvecs;
# // Set coordinate system
# cv::Mat objPoints(4, 1, CV_32FC3);
# ...
# // Calculate pose for each marker
# for (int i = 0; i < nMarkers; i++) {
#     solvePnP(objPoints, corners.at(i), cameraMatrix, distCoeffs, rvecs.at(i), tvecs.at(i));
# }
