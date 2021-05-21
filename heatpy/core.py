import meshio
import numpy as np


class Domain:

    def __init__(self, mesh_file: str = None):
        self.mesh = meshio.read(mesh_file)
