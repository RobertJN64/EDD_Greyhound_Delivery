from util import get_tag_data, get_image, render_3d_tag_pos, get_roll_pitch_yaw, auto_stop
import TKinterModernThemes as TKMT
import tkinter as tk

stream_running = False
ip_addr = '192.168.137.68'

def no_data_round(v):
    if v is None:
        return 'no data'
    else:
        return str(round(v[0], 3))

def generate_xyz_labels(x, y, z):
    return (
        "X (+right): " + no_data_round(x),
        "Y (+down): " + no_data_round(y),
        "Z (+away): " + no_data_round(z)
    )

def generate_rpy_labels(roll, pitch, yaw): #TODO - check if these are correct
    return (
        "Roll (+clockwise): " + no_data_round(roll),
        "Pitch (+top_closer): " + no_data_round(pitch),
        "Yaw (+right_closer): " + no_data_round(yaw)
    )

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
        self.num_id_int = tk.StringVar(value='0')
        buttonframe.Checkbutton('Flip Image', self.flip_bool)
        buttonframe.Checkbutton('Tag View', self.tag_view_bool, col=1)
        buttonframe.Text("Camera ID:")
        buttonframe.Entry(self.num_id_int, col=1)

        targetframe = self.addLabelFrame("Target Pos", col=2)

        targetframe.Label('X:')
        targetframe.Label('Y:')
        targetframe.Label('Z:')
        targetframe.Label('Dist:')
        targetframe.nextCol()
        self.target_x_var = tk.StringVar(value='0.0')
        self.target_y_var = tk.StringVar(value='0.0')
        self.target_z_var = tk.StringVar(value='0.0')
        self.target_dist_var = tk.StringVar(value='0.0')
        targetframe.Entry(self.target_x_var)
        targetframe.Entry(self.target_y_var)
        targetframe.Entry(self.target_z_var)
        targetframe.Entry(self.target_dist_var)

        self.dist_var = tk.StringVar(value="<no data> in. away")
        targetframe.Label('', widgetkwargs={'textvariable': self.dist_var}, col=0, colspan=2)
        self.auto_stop_var = tk.BooleanVar(value=False)
        targetframe.Checkbutton("Auto stop", self.auto_stop_var, col=0)

        tag_data_frame = self.addLabelFrame('Tag Data', col=1)
        self.current_tag_var = tk.StringVar()
        tag_data_frame.OptionMenu(list(map(str, range(0,4))), self.current_tag_var, colspan=2)
        x, z, y = generate_xyz_labels(None, None, None)
        self.tdf_xvar = tk.StringVar(value=x)
        self.tdf_yvar = tk.StringVar(value=y)
        self.tdf_zvar = tk.StringVar(value=z)
        tag_data_frame.Label('', widgetkwargs={'textvariable': self.tdf_xvar}, sticky='w')
        tag_data_frame.Label('', widgetkwargs={'textvariable': self.tdf_yvar}, sticky='w')
        tag_data_frame.Label('', widgetkwargs={'textvariable': self.tdf_zvar}, sticky='w')
        tag_data_frame.nextCol()

        r, p, y = generate_rpy_labels(None, None, None)
        self.tdf_roll_var = tk.StringVar(value=r)
        self.tdf_pitch_var = tk.StringVar(value=p)
        self.tdf_yaw_var = tk.StringVar(value=y)
        tag_data_frame.Label('', widgetkwargs={'textvariable': self.tdf_roll_var}, sticky='w')
        tag_data_frame.Label('', widgetkwargs={'textvariable': self.tdf_pitch_var}, sticky='w')
        tag_data_frame.Label('', widgetkwargs={'textvariable': self.tdf_yaw_var}, sticky='w')

        self.debugPrint()
        self.run()

    def periodic(self):
        self.update_tag_data()
        self.update_camera_feed_image()
        self.root.after(100, self.periodic)  # Call every 0.1 seconds to keep UI updated

    def generate_distance_label(self, cx, cy, cz):
        try:
            tx = float(self.target_x_var.get())
            ty = float(self.target_y_var.get())
            tz = float(self.target_z_var.get())
            td = float(self.target_dist_var.get())

            d = (tx-cx[0])**2 + (ty-cy[0])**2 + (tz-cz[0])**2
            d = d ** 0.5

            s = f"{round(d,3)} in. away"
            if d < td:
                s += " (at target)"
                if self.auto_stop_var.get():
                    auto_stop()
            return s
        except ValueError:
            return "numerical error"


    def update_tag_data(self):
        j = get_tag_data(ip_addr, self.num_id_int.get())
        render_3d_tag_pos(j['ids'], j['tvecs'], j['rvecs'], self.tag_pos_ax)
        self.tag_pos_canvas.draw()

        # region xyz rpy
        for ind, i in enumerate(j['ids']):
            if i[0] == int(self.current_tag_var.get()):
                cx, cy, cz = j['tvecs'][ind]
                cz = [cz[0]/1.6] #hack to fix dist
                x, y, z = generate_xyz_labels(cx, cy, cz) #unpack arr
                roll, pitch, yaw = generate_rpy_labels(*get_roll_pitch_yaw(j['rvecs'][ind]))
                self.dist_var.set(self.generate_distance_label(cx, cy, cz))
                break

        else:
            x, y, z = generate_xyz_labels(None, None, None)
            roll, pitch, yaw = generate_rpy_labels(None, None, None)
            self.dist_var.set("<no data> in. away")


        self.tdf_xvar.set(x)
        self.tdf_yvar.set(y)
        self.tdf_zvar.set(z)

        self.tdf_roll_var.set(roll)
        self.tdf_pitch_var.set(pitch)
        self.tdf_yaw_var.set(yaw)
        #endregion

    def update_camera_feed_image(self):
        imgtk = get_image(ip_addr, num_id=self.num_id_int.get(),
                          tag_view=self.tag_view_bool.get(), flip_vert=self.flip_bool.get())
        self.camera_image.configure(image=imgtk)
        self.camera_image.image = imgtk

    def activate_streams(self):
        global stream_running, ip_addr
        ip_addr = self.ip_addr_tk_var.get()

        if not stream_running:
            self.root.after(100, self.periodic)

        stream_running = True


if __name__ == "__main__":
    App("park", "dark")