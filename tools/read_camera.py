import numpy as np
import requests
import base64
import cv2
import time

def get_image(ip: str):
    jpg_original = base64.b64decode(requests.get('http://' + ip + '/tag_view').text)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    return cv2.imdecode(jpg_as_np, flags=1)

def main():
    while True:
        t = time.time()
        img = get_image('192.168.137.240')
        #img = get_image('127.0.0.1')
        cv2.imshow("Robert Ops", img.copy())
        cv2.waitKey(1)
        print(f"FPS: {round(1 / (time.time() - t), 2)}")

if __name__ == '__main__':
    main()