import numpy as np
import threading
import datetime
import requests
import base64
import time
import cv2

CAM_DONE = False
CAM_BUF = False
CHESS_DONE = False
CHESS_BUF = False
DRAW_DONE = False

cam_img = None
chess_img = None


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
    jpg_original = base64.b64decode(requests.get('http://' + ip + '/camera?w=800&h=640').text)
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

def read_from_camera():
    global cam_img, CAM_DONE, CAM_BUF
    while True:
        cam_img = get_image('192.168.137.240')
        CAM_DONE = True
        while not CAM_BUF:
            time.sleep(0.01)
        CAM_BUF = False

def process_image():
    global chess_img, cam_img, CAM_DONE, CAM_BUF, CHESS_DONE, CHESS_BUF

    while True:
        while not CAM_DONE:
            time.sleep(0.01)
        CAM_DONE = False
        chess_img = cam_img.copy()
        CAM_BUF = True
        chess_img = chessboard(chess_img)
        CHESS_DONE = True
        while not CHESS_BUF:
            time.sleep(0.01)
        CHESS_BUF = False

def draw_img():
    global chess_img, CHESS_DONE, CHESS_BUF

    while True:
        t = time.time()
        while not CHESS_DONE:
            time.sleep(0.01)

        CHESS_DONE = False
        img_to_draw = chess_img.copy()
        CHESS_BUF = True



        cv2.imshow("Robert Ops", img_to_draw)
        k = cv2.waitKey(1)
        print(f"FPS: {round(1 / (time.time() - t), 2)}")

        if k == 27:  # Esc key to stop
            break
        elif k == ord('c'):
            fname = datetime.datetime.now().strftime("%m-%d-%Y %I-%M-%S %p") + '.png'
            print("Saving image as: " + fname)
            print(cv2.imwrite('calib_images/rpi/' + fname, img))

def main():
    threading.Thread(target=read_from_camera).start()
    threading.Thread(target=process_image).start()
    threading.Thread(target=draw_img).start()


if __name__ == '__main__':
    main()