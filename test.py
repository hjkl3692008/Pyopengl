from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np

from tools import trans_tools as tt
from tools import calculate_tools as ct
from tools import file_tools as ft

from model import *
from model import light

a = np.array([[1, 2, 3, 4], [2, 3, 4, 5]])
a = a - 1

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

# normals = ct.cal_all_normals(points, polygons)

a = set(['a','a','b'])
a.update('a', 'c')
print(a)

vertex_name = 'Phong.vertexshader.glsl'
m = light.parameter_dict.get(vertex_name, None)
for key in m.keys():
    print(key)
0