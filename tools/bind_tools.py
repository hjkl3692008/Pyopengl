from OpenGL.GL import *

from tools import trans_tools as tt
from tools import calculate_tools as ct

BIND_VERTEX = 'BIND_VERTEX'
BIND_TWEENED_VERTEX = 'BIND_TWEENED_VERTEX'
BIND_NORMAL = 'BIND_NORMAL'
BIND_INDICES = 'BIND_INDICES'
BIND_UV = 'BIND_UV'


def bind_object(bind_type, vertexes, indices, normals, uv):
    # triangles = tt.polygon2triangle(polygons)
    vertexbuffer = None
    vertex_tweened_buffer = None
    normalbuffer = None
    indicesbuffer = None
    uvbuffer = None

    for bt in bind_type:
        if bt == BIND_VERTEX:
            vertexbuffer = glGenBuffers(1)  # create buffer
            glBindBuffer(GL_ARRAY_BUFFER, vertexbuffer)  # bind
            vertexes_list = vertexes.flatten().tolist()
            glBufferData(GL_ARRAY_BUFFER, len(vertexes_list) * 4, (GLfloat * len(vertexes_list))(*vertexes_list),
                         GL_STATIC_DRAW)
            # glBufferData(GL_ARRAY_BUFFER, vertexes.nbytes, vertexes, GL_STATIC_DRAW)
        if bt == BIND_NORMAL:
            normalbuffer = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, normalbuffer)
            normals_list = normals.flatten().tolist()
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(normals_list) * 4,
                         (GLfloat * len(normals_list))(*normals_list),
                         GL_STATIC_DRAW)
            # glBufferData(GL_ELEMENT_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
        if bt == BIND_INDICES:
            indicesbuffer = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, indicesbuffer)
            indices_list = indices.flatten().tolist()
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices_list) * 2,
                         (GLushort * len(indices_list))(*indices_list),
                         GL_STATIC_DRAW)
            # glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        if bt == BIND_UV:
            uvbuffer = glGenBuffers(1)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, uvbuffer)
            uv_list = uv.flatten().tolist()
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(uv_list) * 4,
                         (GLfloat * len(uv_list))(*uv_list), GL_STATIC_DRAW)
        if bt == BIND_TWEENED_VERTEX:
            vertex_tweened_buffer = glGenBuffers(1)  # create buffer
            glBindBuffer(GL_ARRAY_BUFFER, vertex_tweened_buffer)  # bind
            vertexes_list = vertexes.flatten().tolist()
            ## todo:// other tweened function
            vertexes_tweened_list = [i * 5 for i in vertexes_list]
            glBufferData(GL_ARRAY_BUFFER, len(vertexes_tweened_list) * 4, (GLfloat * len(vertexes_tweened_list))(*vertexes_tweened_list),
                         GL_STATIC_DRAW)

    return vertexbuffer, normalbuffer, indicesbuffer, uvbuffer, vertex_tweened_buffer
