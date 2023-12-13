import matplotlib.pyplot as plt
import requests
import json
import time
import cv2


c_matrix = ['red', 'orange', 'blue', 'black']

def update(ids, tags, tag_rvecs, ax):
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
        rot_matrix = cv2.Rodrigues(rvec)[0]
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
    plt.draw()
    plt.pause(0.01)


def main():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    plt.show(block=False)

    while True:
        t = requests.get('http://127.0.0.1/tag_data').text
        print(t)
        j = json.loads(t)
        update(j['ids'], j['tvecs'], j['rvecs'], ax)
        time.sleep(0.05)
        if not plt.fignum_exists(fig.number):
            break  # handle exit


if __name__ == '__main__':
    main()