import os

import pytest
import meshio

import heatpy


class TestMesh:

    def test_generate_mesh(self):
        heatpy.rec_mesh(0.4, 0.5, filename='test_rectangular.msh')

    def test_visualization(self):
        try:
            mesh = meshio.read(
                os.path.join('test_rectangular.msh')
            )

            heatpy.plot_mesh(mesh)
        finally:
            os.remove('test_rectangular.msh')
