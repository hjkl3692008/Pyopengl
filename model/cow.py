from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from tools import file_tools as ft
from tools import trans_tools as tt
from tools import shader_tools as st
from tools import calculate_tools as ct

from model.basic_object import BasicObject


class Cow(BasicObject):
    is_trans = None
    vertex_shaders = None
    fragment_shaders = None

    def __init__(self, is_trans=True, vertex_shaders=["Phong.vertexshader.glsl"],
                 fragment_shaders=["Phong.fragmentshader.glsl"]):
        self.is_trans = is_trans
        self.vertex_shaders = vertex_shaders
        self.fragment_shaders = fragment_shaders
        super().__init__()

    def load_data(self):
        head, vertexes, indices = ft.load_cow()
        normals = None
        if self.is_trans:
            normals = ct.cal_all_normals(vertexes, indices)
            indices = tt.polygon2triangle(indices)
        return vertexes, indices, normals

    def load_object(self):
        super().load_object()

    def load_shader(self):
        self.shader = st.Shader()
        self.shader.initShader(self.vertex_shaders, self.fragment_shaders)
        self.shader.bind_parameters(self)

    def rendering(self):
        self.shader.begin()
        try:
            self.set_uniform_value()

            glEnableVertexAttribArray(self.Vertex_position_loc)
            glBindBuffer(GL_ARRAY_BUFFER, self.vertexbuffer)
            glVertexAttribPointer(self.Vertex_position_loc, 3, GL_FLOAT, GL_FALSE, 0, None)

            glEnableVertexAttribArray(self.Vertex_normal_loc)
            glBindBuffer(GL_ARRAY_BUFFER, self.normalbuffer)
            glVertexAttribPointer(self.Vertex_normal_loc, 3, GL_FLOAT, GL_FALSE, 0, None)

            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indicesbuffer)

            glDrawElements(
                GL_TRIANGLES,  # draw mode
                self.indices.size,  # count of indices
                GL_UNSIGNED_SHORT,  # type of indices data
                None
            )
        finally:
            glDisableVertexAttribArray(self.Vertex_position_loc)
            glDisableVertexAttribArray(self.Vertex_normal_loc)
            self.shader.end()

    def set_uniform_value(self):
        for uniform in self.shader.uniform_list:
            uniform_value = self.shader.uniform_default_value.get(uniform, None)
            if uniform_value is not None:
                length = len(uniform_value)
                if length == 1:
                    glUniform1f(getattr(self, uniform + '_loc'), uniform_value[0])
                elif length == 2:
                    glUniform2f(getattr(self, uniform + '_loc'), uniform_value[0], uniform_value[1])
                elif length == 3:
                    glUniform3f(getattr(self, uniform + '_loc'), uniform_value[0], uniform_value[1], uniform_value[2])
                elif length == 4:
                    glUniform4f(getattr(self, uniform + '_loc'), uniform_value[0], uniform_value[1], uniform_value[2],
                                uniform_value[3])
