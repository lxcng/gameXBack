from Box2D import *

import numpy as np
import math
# import threading
import gevent
import time
from quadtree import Quadtree
# import redis

speed = 1.0
bulletspeed = 2.0
pixels_per_meter = 200
#
# speed = 1.0;
# bulletspeed = 1.0


class World:
    """World class"""

    def __init__(self):
        self.childs = {}
        self.world = b2World(gravity=(0, 0), doSleep=True, contactListener=myContactListener()) #!!!
        self.fps = 50
        self.timeStep = 1.0 / self.fps
        self.vel_iters = 6
        self.pos_iters = 2
        self.state = 0 #ready
        self.wall_count = 0;
        # self.tree = Quadtree(0, [-500, -500, 1000, 1000])

    def add_player(self, id, position):
        fixtureDef = b2FixtureDef(shape=b2CircleShape(pos=b2Vec2(0.0, 0.0), radius=0.2), density=1.0, groupIndex=1)
        body = self.world.CreateDynamicBody(position=position, fixtures=fixtureDef, userData=Data(id, 'player'))
        self.childs[id] = body

    def add_wall(self, pos, rect):
        fixtureDef = b2FixtureDef(shape=b2PolygonShape(box=rect, pos=b2Vec2(0.0, 0.0)), density=0.0, groupIndex=2)
        body = self.world.CreateStaticBody(position=pos, fixtures=fixtureDef, userData=Data(id, 'wall'))
        self.childs['wall_' + str(self.wall_count)] = body
        self.wall_count += 1

    def add_bullet(self, id, parent, dmg):
        pos = parent.position.copy()
        pos.x += (0.004 + parent.fixtures[0].shape.radius + 0.001) * math.cos(parent.angle)
        pos.y += (0.004 + parent.fixtures[0].shape.radius + 0.001) * math.sin(parent.angle)

        fixtureDef = b2FixtureDef(shape=b2CircleShape(pos=b2Vec2(0.0, 0.0), radius=0.004), density=0.0, groupIndex=3)
        bullet_id = 'bullet_' + str(id) + '_' + str(time.time())
        body = self.world.CreateDynamicBody(position=pos, bullet=True, fixtures=fixtureDef, angle=parent.angle, userData=Data(bullet_id, 'bullet'))
        v = b2Vec2(math.cos(body.angle), math.sin(body.angle))
        v *= bulletspeed
        body.linearVelocity = v
        self.childs[bullet_id] = body
        gevent.spawn(self.bullet_lifespan, bullet_id)

    def bullet_lifespan(self, b):
        gevent.sleep(10.0)
        self.del_child(b)


    def add_door(self, id, pos, rect, orientation):
        fixtureDef = b2FixtureDef(shape=b2PolygonShape(box=rect, pos=b2Vec2(0.0, 0.0)), density=2.0, groupIndex=4)
        body0 = self.world.CreateDynamicBody(position=pos, fixtures=fixtureDef, userData=Data(id, 'door'))

        if orientation == 0:
            pos = (pos[0] - rect[0] + rect[1], pos[1])
            rect = (rect[1], rect[1])
        elif orientation == 2:
            pos = (pos[0] + rect[0] - rect[1], pos[1])
            rect = (rect[1], rect[1])
        elif orientation == 1:
            pos = (pos[0], pos[1] + rect[0] - rect[1])
            rect = (rect[0], rect[0])
        elif orientation == 3:
            pos = (pos[0], pos[1] - rect[0] + rect[1])
            rect = (rect[0], rect[0])
        fixtureDef = b2FixtureDef(shape=b2PolygonShape(box=rect, pos=b2Vec2(0.0, 0.0)), density=2.0, groupIndex=4)
        body1 = self.world.CreateBody(position=pos, fixtures=fixtureDef, userData=Data(id, 'door'))
        joint = self.world.CreateRevoluteJoint(bodyA=body0, bodyB=body1, anchor=body1.worldCenter)
        self.childs[id] = body0
        pass

    def del_child(self, id):
        self.world.DestroyBody(self.childs.pop(id))

    def step(self):
        self.world.Step(self.timeStep, self.vel_iters, self.pos_iters)

        body_pairs = [(p.fixtureA.body, p.fixtureB.body) for p in self.world.contactListener.shot_points]
        self.world.contactListener.clear()
        if len(body_pairs) != 0:
            nuke = []
            for bodyA, bodyB in body_pairs:
                if bodyA.bullet:
                    nuke_body = bodyA
                else:
                    nuke_body = bodyB
                if nuke_body not in nuke:
                    nuke.append(nuke_body)
            for b in nuke:
                # print 'nuke', b.userData.id
                self.del_child(b.userData.id)
            nuke = None

        self.world.ClearForces()

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
            gevent.sleep(self.timeStep)

    def modify_child(self, id, velocity, angle, click):
        pass
        body = self.childs[id]

        # f = body.GetWorldVector(localVector=velocity)
        # if body.fixtures[0].filterData.groupIndex == 1:
        #     f *= speed * 50
        v = b2Vec2(velocity)
        if body.fixtures[0].filterData.groupIndex == 1:
            v *= speed
        # p = body.GetWorldPoint(localPoint=(0.0, 0.0))
        # body.awake = True

        body.linearVelocity = v
        body.angle = angle
        # body.ApplyForce(force=f, point=p, wake=True)
        if click:
            self.add_bullet(id, body, 0.0)

    def world_state(self):
        message = ''
        for key in self.childs:
            body = self.childs[key]
            message += '^' + str(key)
            # message += '^' + str(body.type) + ('', 'b')[body.bullet]
            message += '^' + str(body.userData.type)
            message += '^' + str(int(body.position.x * pixels_per_meter))
            message += '^' + str(int(body.position.y * pixels_per_meter))
            message += '^' + str(body.angle)
            # message += '^' + str(int(math.degrees(body.angle)))
        return message


    def world_state_deb(self):
        message = ''
        for key in self.childs:
            body = self.childs[key]
            message += str(key)
            # message += ' ' + str(body.type) + ('', 'b')[body.bullet]
            message += ' ' + str(body.position.x)
            message += ' ' + str(body.position.y)
            message += ' ' + str(body.angle) + '\n'
        return message


class Data:

    types = {'player': 0,
             'wall': 1,
             'bullet': 2,
             'door': 3}

    def __init__(self, id, typ):
        self.id = id
        self.type = Data.types.get(typ)


class myContactListener(b2ContactListener):

    def __init__(self):
        b2ContactListener.__init__(self)
        self.shot_points = []

    def BeginContact(self, contact):
        pass

    def EndContact(self, contact):
        pass

    def PreSolve(self, contact, oldManifold):
        worldManifold = contact.worldManifold
        state1, state2 = b2GetPointStates(oldManifold, contact.manifold)
        if state2[0] == b2_addState:
            bodyA = contact.fixtureA.body
            bodyB = contact.fixtureB.body
            if bodyA.bullet or bodyB.bullet:
                self.shot_points.append(contact)
            if len(bodyA.joints) != 0 or len(bodyB.joints) != 0:
                pass

    def PostSolve(self, contact, impulse):
        pass

    def clear(self):
        self.shot_points = []

