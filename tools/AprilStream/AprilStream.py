import TKinterModernThemes as TKMT
import requests
import json

from util import render_3d_tag_pos, get_image


class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode):
        super().__init__("April Stream", theme, mode)

        camera_view_frame = self.addLabelFrame("Camera Feed")
        self.camera_image = camera_view_frame.Label('')

        tag_pos_frame = self.addLabelFrame("3D Graph", col=1)
        self.tag_pos_canvas, tag_pos_fig, self.tag_pos_ax, _, _ = tag_pos_frame.matplotlibFrame("Graph 3D", projection='3d')

        buttonframe = self.addLabelFrame("Control Buttons")
        buttonframe.Button("Start Stream", self.activate_streams, colspan=2)

        self.debugPrint()
        self.run()

    def periodic(self):
        self.update_tag_pos()
        self.update_camera_feed_image()
        self.root.after(100, self.periodic)  # Call every 0.1 seconds to keep UI updated


    def update_tag_pos(self):
        #t = requests.get('http://192.168.137.68/tag_data').text
        t = requests.get('http://127.0.0.1/tag_data').text
        #print(t)
        j = json.loads(t)
        render_3d_tag_pos(j['ids'], j['tvecs'], j['rvecs'], self.tag_pos_ax)
        self.tag_pos_canvas.draw()

    def update_camera_feed_image(self):
        imgtk = get_image('127.0.0.1')
        self.camera_image.configure(image=imgtk)
        self.camera_image.image = imgtk

    def activate_streams(self):
        self.root.after(100, self.periodic)

if __name__ == "__main__":
    App("park", "dark")