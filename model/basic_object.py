
from tools import file_tools as ft
from tools import trans_tools as trans_t
from tools import bind_tools as bt
from tools import shader_tools as st
from tools import texture_tools as texture_t


class BasicObject(object):
    vertexes = None
    indices = None
    normals = None
    vertexbuffer = None
    normalbuffer = None
    indicesbuffer = None
    shader = None
    location = None
    rotate = None

    def __init__(self):
        self.vertexes, self.indices, self.normals = self.load_data()

    def load_data(self):
        # print('this function need to implement')
        return None, None, None

    def load_object(self):
        bind_type = [bt.BIND_VERTEX, bt.BIND_NORMAL, bt.BIND_INDICES]
        self.vertexbuffer, self.normalbuffer, self.indicesbuffer = bt.bind_object(bind_type, self.vertexes,
                                                                                  self.indices, self.normals)

    def load_shader(self):
        self.shader = st.Shader()
        self.shader.initShader(
            ['Phong.vertexshader.glsl'], ['Phong.fragmentshader.glsl'])

    def load_texture(self):
        # todo:// add texture
        0

    def rendering(self):
        # todo:// render
        self.shader.begin()
