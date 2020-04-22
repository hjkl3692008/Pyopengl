import numpy as np
import glm

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from OpenGLContext.events.timer import Timer
from OpenGLContext import testingcontext
BaseContext = testingcontext.getInteractive()

from tools import file_tools as ft
from tools import trans_tools as tt
from tools import shader_tools as st
from tools import calculate_tools as ct
from tools import bind_tools as bt
from tools import texture_tools as texture_t

from model.basic_object import BasicObject

class Cow_Animated(BaseContext):

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

    is_trans = None
    vertex_shaders = None
    fragment_shaders = None
    texture_name = None

    def OnInit(self):

        self.is_trans = True
        self.vertex_shaders = [st.ANIMATED_VERTEX_SHADER]
        self.fragment_shaders = [st.ANIMATED_FRAGMENT_SHADER]
        self.texture_name = 'wood.jpg'
        self.time = Timer(duration=2.0, repeating=1)
        self.time.addEventHandler("fraction", self.OnTimerFraction)
        self.time.register(self)
        self.time.start()
        self.vertexes, self.indices, self.normals, self.uv = self.load_data()
        self.load_object()
        self.load_shader()
        self.load_texture()

        self.location = np.array([0.0, 0.0, 0.0])

        self.EYE = np.array([0.0, 0.0, 10.0])
        self.PREF = np.array([0.0, 0.0, -1.0])
        self.vv = np.array([0.0, 1.0, 0.0])
        self.N = (self.PREF - self.EYE) / np.linalg.norm(self.PREF - self.EYE)
        self.U = np.cross(self.N, self.vv) / np.linalg.norm(np.cross(self.N, self.vv))
        self.EYE_UP = np.cross(self.U, self.N)
        self.d = 0.1
        height = 500
        width = 500
        self.half_h = height / 2
        self.f = 100.0
        self.width = width
        self.height = height
        slope = np.sqrt((pow(self.d, 2) + pow((width / 2), 2)))
        self.fov = 2 * np.arctan(self.half_h / slope)
        left_bottom_near = self.EYE + self.d * self.N - self.half_h * self.U - self.half_h * self.EYE_UP
        right_top_near = self.EYE + self.d * self.N + self.half_h * self.U + self.half_h * self.EYE_UP
        self.VIEW = np.array([left_bottom_near[0], right_top_near[0], left_bottom_near[1], right_top_near[1],
                              np.array([self.d]), np.array([self.f])])
        self.LOOK_AT = np.array([0, 0, 0])
        self.ProjectionMatrix = glm.perspective(self.fov,
                                                float(self.width) / float(self.height), self.d, self.f)
        self.ViewMatrix = glm.lookAt(glm.vec3(self.EYE[0], self.EYE[1], self.EYE[2]),
                                     glm.vec3(self.LOOK_AT[0], self.LOOK_AT[1], self.LOOK_AT[2]),
                                     glm.vec3(self.vv[0], self.vv[1], self.vv[2])
                                     )
        self.MVP = self.ProjectionMatrix * self.ViewMatrix * glm.mat4(1.0)


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
        self.vertexbuffer, self.normalbuffer, self.indicesbuffer, self.uvbuffer, self.vertex_tweened_buffer = bt.bind_object(
            bind_type,
            self.vertexes,
            self.indices,
            self.normals, self.uv)
        # super().load_object(bind_type)

    def load_shader(self):
        self.shader = st.Shader()
        self.shader.init_shader(self.vertex_shaders, self.fragment_shaders)
        self.shader.bind_parameters(self)

    def load_texture(self):
        self.texture = texture_t.Texture()
        self.texture.init_texture(self.texture_name)

    def Render(self, mode=0):
        BaseContext.Render(self, mode)
        self.shader.begin()
        try:
            self.set_uniform_value()
            glUniform1f(self.tween_loc, self.tween_fraction)
            glUniformMatrix4fv(self.MVP_loc, 1, GL_FALSE, glm.value_ptr(self.MVP))
            glUniformMatrix4fv(self.ModelMatrix_loc, 1, GL_FALSE, glm.value_ptr(glm.mat4(1.0)))
            glUniformMatrix4fv(self.ViewMatrix_loc, 1, GL_FALSE, glm.value_ptr(self.ViewMatrix))
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

    tween_fraction = 0.0

    def OnTimerFraction(self, event):
        frac = event.fraction()
        if frac > .5:
            frac = 1.0 - frac
        frac *= 2
        self.tween_fraction = frac
        self.triggerRedraw()
        # glutPostRedisplay()

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
