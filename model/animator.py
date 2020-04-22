import numpy as np

class Animator(object):

    def __init__(self):
        self.animated_time = 3 * 1000  # milli second(ms)
        self.step = 100
        self.each_step_time = int(self.animated_time / self.step)
        self.iteration = 0
        self.fraction = 0.0
        self.each_fraction = 1.0 / self.step

    def add_iter(self):
        self.fraction = self.fraction + self.each_fraction
        if self.fraction > 1:
            self.fraction = 1
            self.iteration = self.step
            return 1.0
        else:
            self.iteration = self.iteration + 1
            return self.fraction
