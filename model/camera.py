import numpy as np


class Camera:
    EYE = None  # camera position
    PREF = None  # view direction
    vv = None  # the positive direction of Y-axis

    N = None  # Z-axis of camera space
    U = None  # X-axis of camera space
    EYE_UP = None  # Y-axis of camera space

    # view frustum
    d = None  # near
    h = None  # 1/2 high
    f = None  # far

    # VIEW Frustum
    VIEW = None
    LOOK_AT = None

    def __init__(self, position=np.array([0.0, 0.0, 10.0]), pref=np.array([0.0, 0.0, -1.0]), \
                 vv=np.array([0.0, 1.0, 0.0]), d=2.0, h=2.0, f=100.0):
        self.EYE = position
        self.PREF = pref
        self.vv = vv
        self.N = (self.PREF - self.EYE) / np.linalg.norm(self.PREF - self.EYE)
        self.U = np.cross(self.N, self.vv) / np.linalg.norm(np.cross(self.N, self.vv))
        self.EYE_UP = np.cross(self.U, self.N)
        self.d = d
        self.h = h
        self.f = f
        left_bottom_near = self.EYE + self.d * self.N - self.h * self.U - self.h * self.EYE_UP
        right_top_near = self.EYE + self.d * self.N + self.h * self.U + self.h * self.EYE_UP
        self.VIEW = np.array([left_bottom_near[0], right_top_near[0], left_bottom_near[1], right_top_near[1],\
                              np.array([self.d]), np.array([self.f])])
        # self.VIEW = np.array([-5, 5, -5, 5, self.d, self.f])
        # self.LOOK_AT = self.EYE + self.PREF
        self.LOOK_AT = np.array([0, 0, 0])