from tools import file_tools as ft
from tools import trans_tools as trans_t
from tools import bind_tools as bt
from tools import shader_tools as st
from tools import texture_tools as texture_t


class BasicObject(object):
    vertexes = None
    normals = None
    indices = None
    uv = None

    vertexbuffer = None
    normalbuffer = None
    indicesbuffer = None
    uvbuffer = None
    vertex_tweened_buffer = None

    shader = None
    texture = None
    location = None
    rotate = None

    def __init__(self):
        self.vertexes, self.indices, self.normals, self.uv = self.load_data()

    def load_data(self):
        print('this method need to be implemented')
        pass

    def load_object(self, bind_type=None):
        if bind_type is None:
            bind_type = [bt.BIND_VERTEX, bt.BIND_NORMAL, bt.BIND_INDICES, bt.BIND_UV]
        self.vertexbuffer, self.normalbuffer, self.indicesbuffer, self.uvbuffer, self.vertex_tweened_buffer = bt.bind_object(
            bind_type,
            self.vertexes,
            self.indices,
            self.normals, self.uv)

    def load_shader(self):
        print('load_shader method need to be implemented')
        pass

    def load_texture(self):
        print('load_texture method need to be implemented')
        pass

    def time_function(self, update_f):
        print('time_function method need to be implemented')
        pass

    def rendering(self):
        print('rendering method need to be implemented')
        pass
