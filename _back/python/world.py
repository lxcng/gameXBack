import numpy as np
import math
# import threading
import gevent
import time
from quadtree import Quadtree
# import redis

speed = 7.0;
bulletspeed = 5.0
#
# speed = 1.0;
# bulletspeed = 1.0


class World:
    """World class"""

    def __init__(self):
        self.childs = {}
        self.fps = 50
        self.time_offset = 1.0 / self.fps
        self.state = 0 #ready
        self.tree = Quadtree(0, [-500, -500, 1000, 1000])

    def add_child(self, child):
        self.childs[child.id] = child
        child.set_parent(self)

    def del_child(self, id):
        self.childs.pop(id)

    def step(self):
        # start = time.time()
        self.check_collisions()
        # print 'collisions', time.time() - start
        for key in self.childs:
            self.childs[key].update()

    def check_collisions(self):
        # start = time.time()
        self.tree.clear()
        for v in self.childs.values():
            self.tree.insert(v)
        # print 'tree', time.time() - start

        for v in self.childs.values():
            if v.typ == 'wall':
                continue
            objs = self.tree.retrieve(v)
            objs.remove(v)
            for o in objs:
                # start = time.time()
                Body.collide(v, o)
                # print 'collide', v.typ, o.typ, time.time() - start
        return 0

    def start(self):
        if self.state == 0:
            self.state = 1
            gevent.spawn(self.run)

    def abort(self):
        if self.state == 1:
            self.state = 0

    def run(self):
        while self.state == 1:
            gevent.spawn(self.step)
            gevent.sleep(self.time_offset)

    def modify_child(self, id, velocity, angle, click):
        self.childs[id].modify(velocity, angle, speed)
        if click:
            self.childs[id].fire()

    def world_state(self):
        message = ''
        for key in self.childs:
            body = self.childs[key]
            message += '^' + body.id
            message += '^' + body.typ
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

    def modify(self, velocity, angle, multiplier):
        self.velocity = np.array(velocity) * multiplier
        self.angle = float(angle)
        self.shape.rotate(angle)

    def update(self):
        self.position += self.velocity;
        self.shape.move(self.velocity)

    def set_parent(self, parent):
        self.parent = parent

    def fire(self):
        pos = np.array([self.position[0], self.position[1]])
        pos[0] += (self.shape.radius + 1.1) * math.cos(self.angle)
        pos[1] -= (self.shape.radius + 1.1) * math.sin(self.angle)
        bullet = Body(str(self.id) + '_' + str(time.time()), Circle(pos, 1.0), np.array(pos), 'bullet')
        bullet.modify([math.cos(self.angle), -math.sin(self.angle)], self.angle, bulletspeed)
        # self.angle = 0.0
        self.parent.add_child(bullet)

    def collided(self, vector, o):
        if self.typ == 'pl':
            if o == 'wall' or o == 'pl':
                sc = vector[0] * self.velocity[0] + vector[1] * self.velocity[1]
                if sc < 0:
                    a = (vector[1] * self.velocity[0] - vector[0] * self.velocity[1])/math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
                    n = np.array([vector[1], - vector[0]]) /math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
                    n *= a
                    self.velocity = n

            elif o == 'bullet':
                # - hp
                return 0
        elif self.typ == 'bullet':
            self.parent.del_child(self.id)
        elif self.typ == 'wall':
            return 0
        return 0

    @staticmethod
    def collide(body0, body1):
        if isinstance(body0.shape, Circle) and isinstance(body1.shape, Circle):
            v = body0.shape.anchor - body1.shape.anchor
            if math.sqrt(v[0] * v[0] + v[1] * v[1]) <= body0.shape.radius + body1.shape.radius:
                body0.collided(v, body1.typ)
                body1.collided(-v, body0.typ)
                return
            else:
                return
        # if type(body0.shape) == Rectangle and type(body0.shape) == Rectangle:
        #     p = 0
        #     for v in body0.shape.vertices:
        #         if Body.norm(body1.shape.vertices[0], body1.shape.vertices[1], v) > 0:
        #             p += 1
        #         else :
        #             p -= 1
        #
        if isinstance(body0.shape, Rectangle) and isinstance(body1.shape, Rectangle):
            return

        if isinstance(body0.shape, Circle):
            m = {}
            for i in range(4):
                nn = Body.norm(body1.shape.vertices[i], body1.shape.vertices[(i + 1) % 4], body0.shape.anchor)
                m[i] = nn
                nn -= body0.shape.radius
                if nn > 0:
                    return
            index = 0
            for i in m.keys():
                if m[index] < m[i]:
                    index = i
            v = body1.shape.vertices[index] - body1.shape.vertices[(index + 1) % 4]
            body0.collided(-np.array([v[1], -v[0]]), body1.typ)
            body1.collided(np.array([v[1], -v[0]]), body0.typ)
            return

        if isinstance(body1.shape, Circle):
            m = {}
            for i in range(4):
                nn = Body.norm(body0.shape.vertices[i], body0.shape.vertices[(i + 1) % 4], body1.shape.anchor)
                m[i] = nn
                nn -= body1.shape.radius
                if nn > 0:
                    return
            index = 0
            for i in m.keys():
                if m[index] < m[i]:
                    index = i
            v = body0.shape.vertices[index] - body0.shape.vertices[(index + 1) % 4]
            body0.collided(-np.array([v[1], -v[0]]), body1.typ)
            body1.collided(np.array([v[1], -v[0]]), body0.typ)
            return

    @staticmethod
    def norm(q, w, e):
        a = w[1] - q[1]
        b = q[0] - w[0]
        c = w[0] * q[1] - q[0] * w[1]
        d = (a * e[0] + b * e[1] + c)/ math.sqrt(a * a + b * b)
        return d


class Shape:
    """Polygon class"""

    def __init__(self, anchor):
        self.anchor = np.array(anchor, dtype=float)
        # self.vertices = vertices
        self.bounds = [0, 0, 0, 0]
        self.angle = 0.0

    def rotate(self, angle):
        return 0

    def move(self, delta):
        # self.vertices += delta
        self.anchor += delta
        self.bounds[0] += delta[0]
        self.bounds[1] += delta[1]


class Circle(Shape):

    def __init__(self, anchor, radius):
        # super.__init__(anchor)
        self.anchor = np.array(anchor, dtype=float)
        self.bounds = np.array([anchor[0] - radius, anchor[1] - radius, radius * 2, radius * 2], dtype=float)
        self.radius = radius
        self.angle = 0.0

    def move(self, delta):
        self.anchor += delta
        self.bounds[0] += delta[0]
        self.bounds[1] += delta[1]


class Rectangle(Shape):

    def __init__(self, anchor, width, height):
        self.vertices = np.array([[width / 2.0, height / 2.0], [-width / 2.0, height / 2.0],
                      [-width / 2.0, -height / 2.0], [width / 2.0, -height / 2.0]])
        self.anchor = np.array(anchor, dtype=float)
        self.vertices += self.anchor
        d = math.sqrt(width * width + height * height)
        self.bounds = np.array([anchor[0] - d / 2, anchor[1] - d / 2, d, d], dtype=float)
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

    def move(self, delta):
        self.vertices += delta
        self.anchor += delta
        self.bounds[0] += delta[0]
        self.bounds[1] += delta[1]