import matplotlib.pyplot as plt

def create_env():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    plt.show(block=False)
    return ax

def update(tags, ax):
    ax.clear()
    def render_tag(x, y, z):
        ax.plot([x, x, x, x, x],
                [y-0.5, y-0.5, y+0.5, y+0.5, y-0.5],
                [z-0.5, z+0.5, z+0.5, z-0.5, z-0.5])

    for tag in tags:
        render_tag(*tag)

    tags.append([0,0,0]) #camera pos

    ax.set_xlim(min([tag[0] for tag in tags]) - 10, max([tag[0] for tag in tags]) + 10)
    ax.set_ylim(min([tag[1] for tag in tags]) - 10, max([tag[1] for tag in tags]) + 10)
    ax.set_zlim(min([tag[2] for tag in tags]) - 10, max([tag[2] for tag in tags]) + 10)

    #ax.scatter3D([0],[0],[0], s=10)
    ax.quiver(0, 0, 0, 5, 0, 0)
    plt.draw()
    plt.pause(0.01)

def update_no_tags(ax):
    update([], ax)