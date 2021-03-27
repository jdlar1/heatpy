import matplotlib.pyplot as plt
import numpy as np
import meshio


def plot_mesh(mesh: meshio._mesh.Mesh, save: bool = False):
    """Grafica una malla en 2D

    Args:
        mesh (meshio._mesh.Mesh): Malla de tipo meshio
        save (bool, optional): Guardar el archivo. Defaults to False.
    """

    pts = mesh.points

    try:
        quads = mesh.cells[1].data
    except:
        quads = mesh.cells[0].data

    for quad in quads:

        elms = pts[np.append(quad, quad[0])]

        x = np.append(elms[:, 0], elms[1, 0])
        y = np.append(elms[:, 1], elms[1, 1])

        plt.plot(x, y, c='royalblue')

    plt.xlabel('x [m]')
    plt.ylabel('y [m]')

    plt.gca().set_aspect('equal', adjustable='box')

    if save:
        plt.savefig('mesh.png', dpi = 600)
    plt.plot()
