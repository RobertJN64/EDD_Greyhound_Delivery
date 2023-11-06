import matplotlib.pyplot as plt

def create_env():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    plt.show(block=False)
    return ax

def update(tags, ax):
    ax.clear()
    def render_tag(x, y, z):
        ax.plot([x-1.5, x+1.5, x+1.5, x-1.5, x-1.5],
                [z, z, z, z, z], #camera z = y
                [y-1.5, y-1.5, y+1.5, y+1.5, y-1.5]) #camera y = z

    for tag in tags:
        tag[1] = -tag[1]
        render_tag(*tag)

    tags.append([0,0,0]) #camera pos

    # ax.set_xlim(min([tag[0] for tag in tags]) - 10, max([tag[0] for tag in tags]) + 10)
    # ax.set_ylim(min([tag[2] for tag in tags]) - 10, max([tag[2] for tag in tags]) + 10)
    # ax.set_zlim(min([tag[1] for tag in tags]) - 10, max([tag[1] for tag in tags]) + 10)
    ax.set_xlim(-25, 25)
    ax.set_ylim(-10, 40)
    ax.set_zlim(-25, 25)

    #ax.scatter3D([0],[0],[0], s=10)
    ax.quiver(0, 0, 0, 0, 5, 0)
    plt.draw()
    plt.pause(0.01)

def update_no_tags(ax):
    update([], ax)