import copy
import datetime

import numpy as np
import requests
import base64
import cv2
import time

def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img


def get_image(ip: str):
    jpg_original = base64.b64decode(requests.get('http://' + ip + '/camera').text)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    image_buffer = cv2.imdecode(jpg_as_np, flags=1)
    adjusted = cv2.convertScaleAbs(image_buffer, alpha=1.5, beta=0.5)

    return adjusted

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
        t = time.time()
        img = get_image('192.168.137.240')
        #img = get_image('127.0.0.1')
        cv2.imshow("Robert Ops", chessboard(img))
        k = cv2.waitKey(1)
        print(f"FPS: {round(1 / (time.time() - t), 2)}")

        if k == 27:  # Esc key to stop
            break
        elif k == ord('c'):
            fname = datetime.datetime.now().strftime("%m-%d-%Y %I-%M-%S %p") + '.png'
            print("Saving image as: " + fname)
            print(cv2.imwrite('calib_images/rpi/' + fname, img))


if __name__ == '__main__':
    main()