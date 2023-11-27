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

if __name__ == '__main__':
    while True:
        t = time.time()
        cv2.imshow("Robert Ops", get_image('127.0.0.1'))
        cv2.waitKey(1)
        print(f"FPS: {round(1 / (time.time() - t), 2)}")