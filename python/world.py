import numpy as np
import math
import threading

speed = 7.0;


class World:
    """World class"""

    def __init__(self):
        self.childs = {}
        self.fps = 50
        self.time_offset = 1.0 / self.fps
        self.state = 0 #ready
        self.deleted = []
        # self.speed = 7.0;
        # self.static = {}

    def add_child(self, child):
        self.childs[child.id] = child
        child.set_parent(self)

    def del_child(self, id):
        # self.deleted.append(id)
        self.childs[id].modify([0, 0], 9.999)
        # self.childs[id].position = np.array([-228228.0, -322322.0], dtype=float)
        # threading.Timer(, 1.0)
        self.childs.pop(id)


    def step(self):
        for key in self.childs:
            self.childs[key].update()

    def check_collisions(self):
        return 0

    def start(self):
        if self.state == 0:
            self.state = 1
            self.run()

    def abort(self):
        if self.state == 1:
            self.state = 0

    def run(self):
        if self.state == 1:
            threading.Timer(self.time_offset, self.run).start()
        self.step()

    def modify_child(self, id, velocity, angle):
        self.childs[id].modify(velocity, angle)

    def world_state(self):
        message = ''
        for key in self.childs:
            body = self.childs[key]
            message += '^' + body.id
            message += '^' + str(body.position[0])
            message += '^' + str(body.position[1])
            message += '^' + str(body.angle)
        return message


class Body:
    """Body class"""

    def __init__(self, id, shape, position): #, static):
        self.id = id
        self.shape = shape
        self.position = np.array(position, dtype=float)
        self.angle = 0.0
        self.velocity = np.array([0, 0])
        self.parent = 0
        # self.static = static

    def modify(self, velocity, angle):
        self.velocity = np.array(velocity)
        self.angle = float(angle)
        self.shape.rotate(angle)

    def update(self):
        self.position += self.velocity * speed;
        self.shape.move(self.velocity)

    def set_parent(self, parent):
        self.parent = parent


class Polygon:
    """Polygon class"""

    def __init__(self, anchor, vertices):
        self.anchor = np.array(anchor, dtype=float)
        self.vertices = vertices
        self.angle = 0.0

    def rotate(self, angle):
        self.vertices -= self.anchor
        delta = angle - self.angle
        # self.angle = angle
        s = math.sin(delta)
        c = math.cos(delta)
        for i in np.arange(self.vertices.shape[0]):
            x = self.vertices[i, 0]
            y = self.vertices[i, 1]
            self.vertices[i] = [x * c - y * s,
                                x * s + y * c]
        self.vertices += self.anchor
        # return  0

    def move(self, delta):
        self.vertices += delta
        self.anchor += delta

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
