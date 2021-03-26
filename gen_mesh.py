import os

import numpy as np
import pygalmesh

OUTPUT_DIR = 'mesh_files'
os.chdir(OUTPUT_DIR)

def rec_mesh(x: int, y: int, filename: str = 'rectangular.msh'):
    points = np.array([[0.0, 0.0], [x, 0.0], [x, y], [0.0, y]])
    constraints = [[0, 1], [1, 2], [2, 3], [3, 0]]

    mesh = pygalmesh.generate_2d(
        points,
        constraints,
        max_edge_size=5.0e-2,
        num_lloyd_steps=10,
    )

    mesh.write('rectangular.msh')


rec_mesh(0.5, 0.3)