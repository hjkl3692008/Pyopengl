import numpy as np
import glm

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from tools import file_tools as ft
from tools import trans_tools as tt
from tools import shader_tools as st
from tools import calculate_tools as ct
from tools import bind_tools as bt
from tools import texture_tools as texture_t

from model.basic_object import BasicObject
from model.animator import Animator

class Cow_Animated2(BasicObject):
    is_trans = None
    vertex_shaders = None
    fragment_shaders = None
    texture_name = None
    tween_fraction = 0.0

    def __init__(self, is_trans=True, vertex_shaders=['Phong.vertexshader.glsl'],
                 fragment_shaders=['Phong.fragmentshader.glsl'], texture_name='wood.jpg', animator=Animator()):
        self.is_trans = is_trans
        self.vertex_shaders = vertex_shaders
        self.fragment_shaders = fragment_shaders
        self.texture_name = texture_name
        self.animator = animator
        super().__init__()

    def load_data(self):
        head, vertexes, indices = ft.load_cow()
        normals = None
        if self.is_trans:
            normals = ct.cal_all_normals(vertexes, indices)
            indices = tt.polygon2triangle(indices)
        # todo:// add real uv
        uv = np.random.random((vertexes.shape[0], 2))
        return vertexes, indices, normals, uv

    def load_object(self):
        bind_type = [bt.BIND_VERTEX, bt.BIND_TWEENED_VERTEX, bt.BIND_NORMAL, bt.BIND_INDICES, bt.BIND_UV]
        super().load_object(bind_type)

    def load_shader(self):
        self.shader = st.Shader()
        self.shader.init_shader(self.vertex_shaders, self.fragment_shaders)
        self.shader.bind_parameters(self)

    def load_texture(self):
        self.texture = texture_t.Texture()
        self.texture.init_texture(self.texture_name)

    def time_function(self, timer):
        # self.tween_fraction = np.math.modf(self.tween_fraction + 1 / self.step)[0]
        self.tween_fraction = self.animator.add_iter()
        self.update_f()
        glutTimerFunc(self.animator.each_step_time, self.time_function, timer)

    def rendering(self, window):
        self.shader.begin()
        try:
            self.set_uniform_value()
            glUniform1f(self.tween_loc, self.tween_fraction)
            glUniformMatrix4fv(self.MVP_loc, 1, GL_FALSE, glm.value_ptr(window.camera.MVP))
            glUniformMatrix4fv(self.ModelMatrix_loc, 1, GL_FALSE, glm.value_ptr(glm.mat4(1.0)))
            glUniformMatrix4fv(self.ViewMatrix_loc, 1, GL_FALSE, glm.value_ptr(window.camera.ViewMatrix))
            glUniform3f(self.LOCATION_OFFSET_loc, self.location[0], self.location[1], self.location[2])

            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.texture.textureGLID)
            glUniform1i(self.diffuse_texture_loc, 0)

            glEnableVertexAttribArray(self.Vertex_position_loc)
            glBindBuffer(GL_ARRAY_BUFFER, self.vertexbuffer)
            glVertexAttribPointer(self.Vertex_position_loc, 3, GL_FLOAT, GL_FALSE, 0, None)

            glEnableVertexAttribArray(self.tweened_loc)
            glBindBuffer(GL_ARRAY_BUFFER, self.vertex_tweened_buffer)
            glVertexAttribPointer(self.tweened_loc, 3, GL_FLOAT, GL_FALSE, 0, None)

            glEnableVertexAttribArray(self.Vertex_normal_loc)
            glBindBuffer(GL_ARRAY_BUFFER, self.normalbuffer)
            glVertexAttribPointer(self.Vertex_normal_loc, 3, GL_FLOAT, GL_FALSE, 0, None)

            glEnableVertexAttribArray(self.Vertex_texture_coordinate_loc)
            glBindBuffer(GL_ARRAY_BUFFER, self.uvbuffer)
            glVertexAttribPointer(self.Vertex_texture_coordinate_loc, 2, GL_FLOAT, GL_FALSE, 0, None)

            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indicesbuffer)

            glDrawElements(
                GL_TRIANGLES,  # draw mode
                self.indices.size,  # count of indices
                GL_UNSIGNED_SHORT,  # type of indices data
                None
            )
        finally:
            glDisableVertexAttribArray(self.Vertex_position_loc)
            glDisableVertexAttribArray(self.tweened_loc)
            glDisableVertexAttribArray(self.Vertex_normal_loc)
            glDisableVertexAttribArray(self.Vertex_texture_coordinate_loc)
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
