import numpy as np
import math
# import matplotlib.pyplot as plt


class World:
    """World class"""

    ticks_per_frame = 50

    def __init__(self):
        self.dynamic = {}
        self.static = {}

    def add_child(self, child):
        self.dynamic.update({child.id, child})
        child.set_parent(self)

    def del_child(self, id):
        self.dynamic.pop(id)

    def step(self):
        for c in self.dynamic:
            c.step()

    def check_collisions(self):
        return 0


class Body:
    """Body class"""

    def __init__(self, id, shape, position): #, static):
        self.id = id
        self.shape = shape
        self.position = position
        self.angle = 0.0
        self.velocity = (0, 0)
        self.parent = 0
        # self.static = static


    def step(self):
        self.position += self.velocity

    def set_parent(self, parent):
        self.parent = parent


class Polygon:
    """Polygon class"""

    def __init__(self, anchor, vertices):
        self.anchor = anchor
        self.vertices = vertices
        self.angle = 0.0

    def rotate(self, angle):
        self.vertices -= self.anchor
        delta = angle - self.angle
        self.angle = angle
        s = math.sin(delta)
        c = math.cos(delta)
        for i in np.arange(self.vertices.shape[0]):
            x = self.vertices[i, 0]
            y = self.vertices[i, 1]
            self.vertices[i] = [x * c - y * s,
                                x * s + y * c]
        self.vertices += self.anchor
        # return  0

    @staticmethod
    def circle(anchor, radius):
        v = np.empty((16, 2))
        v[0] = [radius, 0]
        v[4] = [v[0, 1], v[0, 0]]
        v[8] = [-v[0, 0], v[0, 1]]
        v[12] = [v[0, 1], -v[0, 0]]

        v[1] = [radius * math.cos(math.pi / 8), radius * math.sin(math.pi / 8)]
        v[3] = [v[1, 1], v[1, 0]]
        v[5] = [-v[1, 1], v[1, 0]]
        v[7] = [-v[1, 0], v[1, 1]]
        v[9] = [-v[1, 0], -v[1, 1]]
        v[11] = [-v[1, 1], -v[1, 0]]
        v[13] = [v[1, 1], -v[1, 0]]
        v[15] = [v[1, 0], -v[1, 1]]

        v[2] = [radius * math.cos(math.pi / 4), radius * math.sin(math.pi / 4)]
        v[6] = [-v[2, 0], v[2, 1]]
        v[10] = [-v[2, 0], -v[2, 1]]
        v[14] = [v[2, 0], -v[2, 1]]

        v += anchor
        c = Polygon(anchor, v)
        return c

    @staticmethod
    def rectangle(anchor, width, height):
        v = np.array([[width / 2.0, height / 2.0], [-width / 2.0, height / 2.0],
                      [-width / 2.0, -height / 2.0], [width / 2.0, -height / 2.0]])
        v += anchor
        r = Polygon(anchor, v)
        return r
