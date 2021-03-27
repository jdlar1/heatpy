import os
import glob

import pytest
import meshio

import heatpy


class TestMeshes:

    def test_open_mesh_files(self):

        files = glob.glob(os.path.join('.', 'mesh_files', '*'))

        print(files)

        for mesh_file in files:
            meshio.read(mesh_file)