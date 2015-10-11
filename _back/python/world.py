import numpy as np
import math
import threading
import gevent
# import redis

speed = 7.0;


class World:
    """World class"""

    def __init__(self):
        self.childs = {}
        self.fps = 50
        self.time_offset = 1.0 / self.fps
        self.state = 0 #ready

    def add_child(self, child):
        self.childs[child.id] = child
        child.set_parent(self)

    def del_child(self, id):
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
        self.step()#


    # def start(self):
    #     if self.state == 0:
    #         self.state = 1
    #         tred = gevent.spawn(self.loop)
    #
    # def loop(self):
    #     while self.state == 1:
    #         gevent.spawn(self.step)
    #         gevent.sleep(self.time_offset)
    #
    # def abort(self):
    #     if self.state == 1:
    #         self.state = 0

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

    def __init__(self, id, shape, position, typ):
        self.id = id
        self.shape = shape
        self.position = np.array(position, dtype=float)
        self.typ = typ
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
        self.bounds = [0, 0, 0, 0]
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
        self.bounds[0] += delta[0]
        self.bounds[1] += delta[1]

    @staticmethod
    def circle(anchor, radius):
        v = np.array([radius])

        v += anchor
        c = Polygon(anchor, v)
        c.bounds = [anchor[0] - radius, anchor[1] - radius, radius * 2, radius * 2]
        return c

    @staticmethod
    def rectangle(anchor, width, height):
        v = np.array([[width / 2.0, height / 2.0], [-width / 2.0, height / 2.0],
                      [-width / 2.0, -height / 2.0], [width / 2.0, -height / 2.0]])
        v += anchor
        r = Polygon(anchor, v)
        r.bounds = [anchor[0], anchor[1], width, height]
        return r
