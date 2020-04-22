from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np
import glm

from tools import trans_tools as tt
from tools import calculate_tools as ct
from tools import file_tools as ft

from model import *
from model import light
from model import windows


def test_normal():
    points = np.array([
        [1.0, 1.0, 1.0],
        [1.0, 1.0, -1.0],
        [-1.0, 1.0, 1.0],
        [-1.0, 1.0, -1.0],
        [1.0, -1.0, 1.0],
        [1.0, -1.0, -1.0],
        [-1.0, -1.0, 1.0],
        [-1.0, -1.0, -1.0]
    ])

    polygons = np.array([
        [3, 0, 1, 3, 2],
        [3, 0, 4, 5, 1],
        [3, 1, 5, 7, 3],
        [3, 2, 3, 7, 6],
        [3, 0, 2, 6, 4],
        [3, 4, 6, 7, 5]
    ])

    polygons = polygons + 1

    normals = ct.cal_all_normals(points, polygons)


# print(np.arctan(1))

# dict = {'a': 1, 'b': None}
# c = dict.get('b')
# print(c is None)

# d = glm.vec3(5, 5, 5)
# d1 = glm.lookAt(d,
#                 d,
#                 d
#                 )

x = 1.5
print(np.modf(x)[0])

0
