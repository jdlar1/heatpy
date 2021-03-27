import os

import numpy as np
import pygalmesh


def rec_mesh(x: int, y: int, filename: str = 'rectangular.msh'):

    path = os.path.normpath(filename)
    """Genera el mallado de un objeto rectangular de dimensiones x * y

    Args:
        x (int): medida en x (metros)
        y (int): medida en y (metros)
        filename (str, optional): nombre del archivo. Defaults to 'rectangular.msh'.
        out_dir (str, optional): directorio en el cual está el archivo. Defaults to 'mesh_files'.
    """

    points = np.array([[0.0, 0.0], [x, 0.0], [x, y], [0.0, y]])
    constraints = [[0, 1], [1, 2], [2, 3], [3, 0]]

    mesh = pygalmesh.generate_2d(
        points,
        constraints,
        max_edge_size=5.0e-2,
        num_lloyd_steps=10,
    )

    mesh.write(path)
