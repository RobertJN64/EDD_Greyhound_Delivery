from util import get_and_render_tags, get_image
import TKinterModernThemes as TKMT
import tkinter as tk

stream_running = False
ip_addr = '127.0.0.1'

class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode):
        super().__init__("April Stream", theme, mode)

        camera_view_frame = self.addLabelFrame("Camera Feed")
        self.camera_image = camera_view_frame.Label('')

        tag_pos_frame = self.addLabelFrame("3D Graph", col=1)
        self.tag_pos_canvas, tag_pos_fig, self.tag_pos_ax, _, _ = tag_pos_frame.matplotlibFrame("Graph 3D", projection='3d')

        buttonframe = self.addLabelFrame("Control Buttons")
        self.ip_addr_tk_var = tk.StringVar(value = ip_addr)
        buttonframe.Entry(self.ip_addr_tk_var)
        buttonframe.Button("Start Stream", self.activate_streams, col=1)
        self.flip_bool = tk.BooleanVar(value=False)
        self.tag_view_bool = tk.BooleanVar(value=True)
        buttonframe.Checkbutton('Flip Image', self.flip_bool)
        buttonframe.Checkbutton('Tag View', self.tag_view_bool, col=1)

        tag_data_frame = self.addLabelFrame('Tag Data', col=1)
        self.current_tag_var = tk.StringVar()
        tag_data_frame.OptionMenu(['1', '2', '3', '4'], self.current_tag_var)

        self.debugPrint()
        self.run()

    def periodic(self):
        self.update_tag_pos()
        self.update_camera_feed_image()
        self.root.after(100, self.periodic)  # Call every 0.1 seconds to keep UI updated


    def update_tag_pos(self):
        get_and_render_tags(ip_addr, self.tag_pos_ax)
        self.tag_pos_canvas.draw()
        print(self.current_tag_var.get())

    def update_camera_feed_image(self):
        imgtk = get_image(ip_addr, tag_view=self.tag_view_bool.get(), flip_vert=self.flip_bool.get())
        self.camera_image.configure(image=imgtk)
        self.camera_image.image = imgtk

    def activate_streams(self):
        global stream_running, ip_addr
        ip_addr = self.ip_addr_tk_var.get()

        if not stream_running:
            self.root.after(100, self.periodic)

        stream_running = True

    def update_tag_frame(self):
        pass #do


if __name__ == "__main__":
    App("park", "dark")