import read_camera
import datetime
import cv2

CHECKERBOARD = (5, 5)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

def chessboard(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD,
                                             cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
    if ret:
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        return cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
    else:
        return img

def main():
    while True:
        img = read_camera.get_image('192.168.137.240/camera')
        #img = get_image('127.0.0.1')
        cv2.imshow("Robert Ops", chessboard(img.copy()))
        k = cv2.waitKey(1)
        if k == 27:  # Esc key to stop
            break
        elif k == ord('c'):
            fname = datetime.datetime.now().strftime("%m-%d-%Y %I-%M-%S %p") + '.png'
            print("Saving image as: " + fname)
            print(cv2.imwrite('calib_images/rpi/' + fname, img))

if __name__ == '__main__':
    main()