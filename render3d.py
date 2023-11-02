import matplotlib.pyplot as plt

def plot_3d_enviroment():
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], [0.5, 0.5, 0.5, 0.5, 0.5])

    plt.show()

plot_3d_enviroment()