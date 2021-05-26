import os

import meshio
import numpy as np
import sympy as sym

from sympy.abc import x


class Domain:

    def __init__(self, mesh_file: str = None):
        self.mesh = meshio.read(mesh_file)

        self.points = self.mesh.points
        self.quads = self.mesh.cells[1].data

        self.b_cond = np.array(set(self.mesh.cells[0].data.flatten()))
        print('Nodos con condición de frontera: ')
        print(self.b_cond)

        self.config = {}

    def set(self, payload):
        self.config.update(payload)

    def solve(self, output_dir = ''):

        E = sym.Symbol('E')
        N = sym.Symbol('N')

        n_nodes = self.points.shape[0]
        n_elems = self.quads.shape[0]

        O0 = 1 - E - N
        O1 = E
        O2 = N

        Ht = sym.Matrix([O0, O1, O2])
        H = Ht.T

        D = sym.Matrix([[-1, 1, 0],
                        [-1, 0, 1]])

        def F(i, j):
            x = coord_e[i, j]
            # Aquí se define la función que se desea solucionar.
            f_x = np.sin(float(x))
            return 0  # f_x

        dx = 0

        for i in range(n_nodes-1):
            nx = abs(self.points[i+1, 0])-abs(self.points[i, 0])
            ny = abs(self.points[i+1, 1])-abs(self.points[i, 1])
            if nx > dx:
                dx = nx
            if ny > dx:
                dx = ny

        # 0.0001 determinacion del dt
        dt = (dx**2)/(self.config['alpha']*1000)

        print(f'Delta time is: {dt}')

        for n in range(n_elems):  # n1, n2, n3 y n4 son los nodos que conforman el elemento

            print(f'iterating for element {n + 1}/{n_elems}')

            n1 = int(self.quads[n, 0])
            n2 = int(self.quads[n, 1])
            n3 = int(self.quads[n, 2])

            coord_e = sym.Matrix([self.points[n1, 0:2],
                                  self.points[n2, 0:2],
                                  self.points[n3, 0:2]])

            jm = D*coord_e  # matriz del jacobiano para cada elemento
            jd = jm.det()
            J = jd  # matriz con las magnitudes de los jacobianos

            Jinv = (jm)**-1

            B = Jinv*D

            Bt = B.T
            dK = (Bt*B*J)
            Ke = dK.integrate((E, 0, 1 - N), (N, 0, 1))

            Kg = self.config['alpha']*(np.zeros((n_nodes, n_nodes)))

            for i in range(0, n_elems):
                for j in range(0, 3):
                    for k in range(0, 3):
                        m = self.quads[i, j]
                        n = self.quads[i, k]
                        Kg[m, n] = Kg[m, n] + Ke[j, k]

            Be = np.zeros(3)

            for i in range(0, 3):
                for j in range(0, 2):
                    dB = (Ht[i]*J*F(i, j))
                    w = dB.integrate((E, 0, 1 - N), (N, 0, 1))
                    Be[i] = w

            Bg = np.zeros(n_nodes)

            for i in range(0, n_elems):
                for j in range(0, 3):
                    m = self.quads[i, j]
                    r = Bg[m] + Be[j]
                    Bg[m] = r

            dM = (Ht*H*J)
            Me = dM.integrate((E, 0, 1 - N), (N, 0, 1))

            Mg = np.zeros((n_nodes, n_nodes))

            for i in range(0, n_elems):
                for j in range(0, 3):
                    for k in range(0, 3):
                        z = self.quads[i, j]
                        r = self.quads[i, k]
                        Mg[z, r] = Mg[z, r] + Me[j, k]

        U = np.zeros((n_nodes))
        for i in range(n_nodes):
            U[i] = self.config['init_temp']

        Mr = Mg.copy()
        for i in range(self.b_cond.shape[0]):
            Mr[self.b_cond[i], :] = 0
            Mr[self.b_cond[i], self.b_cond[i]] = 1

        A = -dt*Kg + Mg  # -
        B = dt*Bg

        for i in range(self.config['iterations']):

            C = np.dot(A, U) + B
            for j in range(self.b_cond.shape[0]):
                C[self.b_cond[j]] = self.config['bound_temp']
            Sol = np.linalg.solve(Mr, C)
            U = Sol.copy()

            if True:
                point_data = {'temperature': U}
                triangle_mesh = {
                    'points': self.points,
                    'cells':[("triangle", self.quads)]}

                meshio.write_points_cells(os.path.join(output_dir,f'solution{i}.vtk'),
                             self.points, [('triangle', self.quads.tolist())] , point_data=point_data)

        print(Sol)
