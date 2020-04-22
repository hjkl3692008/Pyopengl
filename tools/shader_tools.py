from OpenGL.GL import *
from OpenGL.raw.GLU import gluErrorString
from OpenGL.GL import shaders

from tools import file_tools as ft
from model import light

PHONG_VERTEX_SHADER = 'Phong.vertexshader.glsl'
PHONG_FRAGMENT_SHADER = 'Phong.fragmentshader.glsl'
GOURAUD_VERTEX_SHADER = 'Gouraud.vertexshader.glsl'
GOURAUD_FRAGMENT_SHADER = 'Gouraud.fragmentshader.glsl'
FLAT_VERTEX_SHADER = 'Flat.vertexshader.glsl'
FLAT_FRAGMENT_SHADER = 'Flat.fragmentshader.glsl'
TEXTURE_VERTEX_SHADER = 'Texture.vertexshader.glsl'
TEXTURE_FRAGMENT_SHADER = 'Texture.fragmentshader.glsl'
ANIMATED_VERTEX_SHADER = 'Animated.vertexshader.glsl'
ANIMATED_FRAGMENT_SHADER = 'Animated.fragmentshader.glsl'


class Shader(object):
    vertex_shader_names = None
    fragment_shader_names = None
    uniform_list = None
    attribute_list = None
    uniform_default_value = None

    def init_shader(self, vertex_shader_names, fragment_shader_names):

        self.vertex_shader_names = vertex_shader_names
        self.fragment_shader_names = fragment_shader_names
        self.uniform_list = set()
        self.attribute_list = set()
        vertex_shader_source_list, fragment_shader_source_list = ft.load_shader_file(vertex_shader_names,
                                                                                     fragment_shader_names)

        # create program
        self.program = glCreateProgram()

        # vertex shader
        # print('compile vertex shader...')
        self.vs = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(self.vs, vertex_shader_source_list)
        glCompileShader(self.vs)
        if GL_TRUE != glGetShaderiv(self.vs, GL_COMPILE_STATUS):
            err_s = glGetShaderInfoLog(self.vs)
            raise Exception(err_s)
        glAttachShader(self.program, self.vs)

        # fragment shader
        # print('compile fragment shader...')
        self.fs = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(self.fs, fragment_shader_source_list)
        glCompileShader(self.fs)
        if GL_TRUE != glGetShaderiv(self.fs, GL_COMPILE_STATUS):
            err_s = glGetShaderInfoLog(self.fs)
            raise Exception(err_s)
        glAttachShader(self.program, self.fs)

        # print('link...')
        glLinkProgram(self.program)
        if GL_TRUE != glGetProgramiv(self.program, GL_LINK_STATUS):
            err_s = glGetShaderInfoLog(self.vs)
            raise Exception(err_s)

    def bind_parameters(self, w_object):
        # get uniform and attribute set
        self.shader_parameters()

        # get id of uniform and attribute
        for uniform in self.uniform_list:
            location = glGetUniformLocation(self.program, uniform)
            if location in (None, -1):
                print('Warning, no uniform: %s' % uniform)
            setattr(w_object, uniform + '_loc', location)
        for attribute in self.attribute_list:
            location = glGetAttribLocation(self.program, attribute)
            if location in (None, -1):
                print('Warning, no attribute: %s' % attribute)
            setattr(w_object, attribute + '_loc', location)

        # get default value of uniform
        uniform_default_value = {}
        for vertex_name in self.vertex_shader_names:
            default_value_dict = light.parameter_dict.get(vertex_name, None)
            if default_value_dict is not None:
                for uniform in self.uniform_list:
                    default_value = default_value_dict.get(uniform, None)
                    # if default_value is not None && not contain this value, add this
                    if (default_value is not None) and (uniform not in uniform_default_value):
                        uniform_default_value[uniform] = default_value
        self.uniform_default_value = uniform_default_value

    def shader_parameters(self):
        for vertex_name in self.vertex_shader_names:
            default_value_dict = light.parameter_dict.get(vertex_name, None)
            if default_value_dict is not None:
                parameter_name_list = []
                for key in default_value_dict.keys():
                    parameter_name_list.append(key)
                self.set_add_elements(self.uniform_list, parameter_name_list)
        for fragment_name in self.fragment_shader_names:
            default_value_dict = light.parameter_dict.get(fragment_name, None)
            if default_value_dict is not None:
                parameter_name_list = []
                for key in default_value_dict.keys():
                    parameter_name_list.append(key)
                self.set_add_elements(self.attribute_list, parameter_name_list)

    def set_add_elements(self, s, elements):
        for e in elements:
            s.add(e)

    def begin(self):
        if glUseProgram(self.program):
            err_s = glGetError()
            if err_s != GL_NO_ERROR:
                print('GLERROR: ', gluErrorString(err_s))

    @staticmethod
    def end():
        glUseProgram(0)
