import TKinterModernThemes as TKMT
from PIL import Image, ImageTk
import numpy as np
import requests
import base64
import json
import cv2


from render_3d_util import render_3d_tag_pos

def get_image(ip: str):
    jpg_original = base64.b64decode(requests.get('http://' + ip).text)
    jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    return cv2.imdecode(jpg_as_np, flags=1)

class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode):
        super().__init__("April Stream", theme, mode)

        self.camera_view_frame = self.addLabelFrame("Camera Feed")

        img = get_image('127.0.0.1/tag_view')
        im = Image.fromarray(img, mode='RGB')
        imgtk = ImageTk.PhotoImage(image=im)
        self.camera_image = self.camera_view_frame.Label('', widgetkwargs={'image': imgtk})

        self.tag_pos_frame = self.addLabelFrame("3D Graph", col=1)
        self.tag_pos_canvas, tag_pos_fig, self.tag_pos_ax, _, _ = self.tag_pos_frame.matplotlibFrame("Graph 3D", projection='3d')
        buttonframe = self.addLabelFrame("Control Buttons")
        buttonframe.Button("???", self.do_nothing, colspan=2)
        self.debugPrint()

        self.root.after(100, self.periodic)
        self.run()

    def periodic(self):
        self.update_tag_pos()
        self.update_camera_feed_image()
        self.root.after(100, self.periodic)  # Call every 0.1 seconds to keep UI updated


    def update_tag_pos(self):
        #t = requests.get('http://192.168.137.68/tag_data').text
        t = requests.get('http://127.0.0.1/tag_data').text
        print(t)
        j = json.loads(t)
        render_3d_tag_pos(j['ids'], j['tvecs'], j['rvecs'], self.tag_pos_ax)
        self.tag_pos_canvas.draw()

    def update_camera_feed_image(self):
        img = get_image('127.0.0.1/tag_view')
        im = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=im)
        self.camera_image.configure(image=imgtk)
        self.camera_image.image = imgtk

    def do_nothing(self):
        pass

if __name__ == "__main__":
    App("park", "dark")