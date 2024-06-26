import math

from PIL import Image, ImageTk
import numpy as np
import requests
import base64
import json
import cv2

def get_image(ip: str, num_id = '0', tag_view = True, flip_vert = False, chessboard = False):
    if num_id == '':
        num_id = '0'

    if tag_view:
        addr = 'http://' + ip + '/tag_view'
    else:
        addr = 'http://' + ip + '/camera'

    addr += '?id=' + num_id

    jpg_original = base64.b64decode(requests.get(addr).text)
    cv2_img = cv2.imdecode(np.frombuffer(jpg_original, dtype=np.uint8), flags=1)

    if flip_vert:
        cv2_img = cv2.flip(cv2_img, 0)

    raw = cv2_img
    if chessboard:
        cv2_img = draw_chessboard(cv2_img.copy())

    return ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB))), raw

c_matrix = ['red', 'orange', 'blue', 'black']

def render_3d_tag_pos(ids, tags, tag_rvecs, ax):
    ax.clear()
    def compute_corner_offset(xbase, ybase, zbase, xoff, yoff, zoff, rot):
        return (
            rot[0][0] * xoff + rot[0][1] * yoff + rot[0][2] * zoff + xbase,
            rot[1][0] * xoff + rot[1][1] * yoff + rot[1][2] * zoff + ybase,
            rot[2][0] * xoff + rot[2][1] * yoff + rot[2][2] * zoff + zbase
        )

    def render_tag(x, y, z, rot, color):
        xd = [-1.5, 1.5, 1.5, -1.5, -1.5]
        yd = [-1.5, -1.5, 1.5, 1.5, -1.5]
        zd = [0, 0, 0, 0, 0]

        xs = []
        ys = []
        zs = []

        for i in range(0, 5):
            xdd, ydd, zdd = compute_corner_offset(x, y, z, xd[i], yd[i], zd[i], rot)
            xs.append(xdd)
            ys.append(-ydd)
            zs.append(zdd)

        ax.plot(xs, zs, ys, c=color) #camera y = z

    for index, tag, rvec in zip(ids, tags, tag_rvecs):
        rot_matrix = cv2.Rodrigues(np.array(rvec))[0]
        render_tag(*tag, rot_matrix, c_matrix[index[0]])

    #tags.append([0,0,0]) #camera pos
    # ax.set_xlim(min([tag[0] for tag in tags]) - 10, max([tag[0] for tag in tags]) + 10)
    # ax.set_ylim(min([tag[2] for tag in tags]) - 10, max([tag[2] for tag in tags]) + 10)
    # ax.set_zlim(min([tag[1] for tag in tags]) - 10, max([tag[1] for tag in tags]) + 10)
    ax.set_xlim(-25, 25)
    ax.set_ylim(-10, 40)
    ax.set_zlim(-5, 45)

    #ax.scatter3D([0],[0],[0], s=10)
    ax.quiver(0, 0, 0, 0, 5, 0)

def get_tag_data(ip: str, num_id = '0'):
    if num_id == '':
        num_id = '0'

    t = requests.get('http://' + ip + '/tag_data?id=' + num_id).text
    return json.loads(t)

def get_roll_pitch_yaw(rvec):
    rot_matrix = cv2.Rodrigues(np.array(rvec))[0]

    # https://en.wikipedia.org/wiki/Rotation_formalisms_in_three_dimensions#Rotation_matrix_.E2.86.94_Euler_angles
    roll = math.atan2(rot_matrix[3-1][1-1], rot_matrix[3-1][2-1])
    pitch = math.acos(rot_matrix[3-1][3-1])
    yaw = -math.atan2(rot_matrix[1-1][3-1], rot_matrix[2-1][3-1])

    return [math.degrees(roll)],[math.degrees(pitch)],[math.degrees(yaw)]

def auto_stop():
    requests.get('http://192.168.137.68/webcontroller/call_method/robot.stop_IMU_drive')

CHECKERBOARD = (5, 5)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

def draw_chessboard(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD,
                                             cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
    if ret:
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        return cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
    else:
        return img