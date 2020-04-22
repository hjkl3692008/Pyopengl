from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np
import glm

from model import *


class Window:
    WIN_W, WIN_H = None, None
    IS_PERSPECTIVE = None  # perspective mode
    SCALE_K = None  # scale of model
    w_objects = []  # object list
    camera = None
    mouse = None
    w_controller = None
    update_function = None

    def __init__(self, win_w=800, win_h=600, is_perspective=True, scale_k=np.array([1.0, 1.0, 1.0])):
        self.WIN_W = win_w
        self.WIN_H = win_h
        self.IS_PERSPECTIVE = is_perspective
        self.SCALE_K = scale_k
        self.camera = camera.Camera()
        self.mouse = mouse.Mouse()
        self.update_function = GLUT.glutPostRedisplay
        self.w_controller = controller.Controller(self, update_f=self.update_function)

    def mouseclick(self, *args, **kwargs):
        if self.w_controller is not None:
            self.w_controller.mouseclick(*args, **kwargs)

    def mousemotion(self, *args, **kwargs):
        if self.w_controller is not None:
            self.w_controller.mousemotion(*args, **kwargs)

    def keydown(self, *args, **kwargs):
        if self.w_controller is not None:
            self.w_controller.keydown(*args, **kwargs)

    def init(self, window_name='window'):
        glutInit()
        displayMode = GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH
        glutInitDisplayMode(displayMode)

        glutInitWindowSize(self.WIN_W, self.WIN_H)
        glutInitWindowPosition(300, 200)
        glutCreateWindow(window_name)

        glClearColor(0.0, 0.0, 0.0, 1.0)  # set background color
        glEnable(GL_DEPTH_TEST)  # enable blocking- z-buffer
        glDepthFunc(GL_LEQUAL)  # blocking type
        glEnable(GL_CULL_FACE)  # cull face
        # glShadeModel(GL_FLAT)  # shade mode: GL_SMOOTH, GL_FLAT

        glutDisplayFunc(self.display)  # display - call back function

        # put below three lines in draw function
        # glRotatef(1, 0, 1, 0)
        # draw something
        # glFlush()

        # create an animation
        # glutIdleFunc(draw)

        glutMouseFunc(self.mouseclick)  # mouse click
        glutMotionFunc(self.mousemotion)  # mouse motion
        glutKeyboardFunc(self.keydown)  # key down

    def add_object(self, w_object, location=np.array([0.0, 0.0, 0.0]), rotate=np.array([0, 0.0, 0.0, 0.0])):
        w_object.load_object()
        w_object.load_shader()
        w_object.load_texture()
        w_object.update_f = self.update_function
        w_object.time_function(1)
        w_object.location = location
        w_object.rotate = rotate
        self.w_objects.append(w_object)

    def display(self):

        # polygonMode
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # clear window & depth buffer
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # enable projection (GL_PROJECTION, GL_MODELVIEW, GL_TEXTURE)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()

        if self.WIN_W > self.WIN_H:
            if self.IS_PERSPECTIVE:
                glFrustum(self.camera.VIEW[0] * self.WIN_W / self.WIN_H, self.camera.VIEW[1] * self.WIN_W / self.WIN_H,
                          self.camera.VIEW[2],
                          self.camera.VIEW[3], self.camera.VIEW[4], self.camera.VIEW[5])
            else:
                glOrtho(self.camera.VIEW[0] * self.WIN_W / self.WIN_H, self.camera.VIEW[1] * self.WIN_W / self.WIN_H,
                        self.camera.VIEW[2],
                        self.camera.VIEW[3],
                        self.camera.VIEW[4], self.camera.VIEW[5])
        else:
            if self.IS_PERSPECTIVE:
                glFrustum(self.camera.VIEW[0], self.camera.VIEW[1], self.camera.VIEW[2] * self.WIN_H / self.WIN_W,
                          self.camera.VIEW[3] * self.WIN_H / self.WIN_W, self.camera.VIEW[4], self.camera.VIEW[5])
            else:
                glOrtho(self.camera.VIEW[0], self.camera.VIEW[1], self.camera.VIEW[2] * self.WIN_H / self.WIN_W,
                        self.camera.VIEW[3] * self.WIN_H / self.WIN_W,
                        self.camera.VIEW[4], self.camera.VIEW[5])

        # change scale
        glScale(self.SCALE_K[0], self.SCALE_K[1], self.SCALE_K[2])

        # set view point
        # gluLookAt(
        #     self.camera.EYE[0], self.camera.EYE[1], self.camera.EYE[2],
        #     self.camera.LOOK_AT[0], self.camera.LOOK_AT[1], self.camera.LOOK_AT[2],
        #     self.camera.EYE_UP[0], self.camera.EYE_UP[1], self.camera.EYE_UP[2]
        # )

        # set view window
        glViewport(0, 0, self.WIN_W, self.WIN_H)

        self.camera.calcMVP(glm.mat4(1.0))

        if len(self.w_objects) != 0:
            for w_object in self.w_objects:
                glPushMatrix()
                if w_object.location is not None:
                    # translate
                    glTranslatef(w_object.location[0], w_object.location[1], w_object.location[2])
                if w_object.rotate is not None:
                    # rotate
                    glRotatef(w_object.rotate[0], w_object.rotate[1], w_object.rotate[2], w_object.rotate[3])  # angle, x, y ,z
                w_object.rendering(self)
                glPopMatrix()
        glutSwapBuffers()

    def run(self):
        glutMainLoop()  # start glut main loop
