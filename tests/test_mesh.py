import os
import glob

import pytest
import meshio

import heatpy


class TestMeshes:

    def test_open_mesh_files(self):

        meshes = []
        files = glob.glob(os.path.join('.', 'mesh_files', '*.vtk'))

        print(files)

        for mesh_file in files:
            m = meshio.read(mesh_file)
            meshes.append(m)
