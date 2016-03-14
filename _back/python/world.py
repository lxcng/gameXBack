from Box2D import *
# import

import math
import gevent
import random
import Queue
import struct
from struct import pack

speed = 1.0
bulletspeed = 2.0
pixels_per_meter = 200


class World:
    """World class"""

    def __init__(self):
        self.world = b2World(gravity=(0, 0), doSleep=True, contactListener=myContactListener()) #!!!
        self.fps = 50
        self.timeStep = 1.0 / self.fps
        self.vel_iters = 6
        self.pos_iters = 2

        self.state = 0 #ready
        self.yaml = ''

        self.wall_seed = 0
        self.door_seed = 0
        self.spawn_seed = 0
        self.bullet_seed = 0
        self.id_seed = 0

        self.ids = Queue.Queue()
        self.ids.maxsize = 2 ** 10
        for i in range(0, 2 ** 10):
            self.ids.put(i)

        self.childs = {}
        self.player_spawns = []
        self.item_spawns = []

    def gen_id(self, type):
        id = 0
        if type == 'player':
            id += 0
        elif type == 'wall':
            id += 1
        elif type == 'bullet':
            id += 2
        elif type == 'door':
            id += 3
        elif type == 'spawn':
            id += 4
        id <<= 10
        # print bin(id)
        id += self.ids.get()
        # print bin(id)
        return id

    def add_player(self, name, position):
        fixtureDef = b2FixtureDef(shape=b2CircleShape(pos=b2Vec2(0.0, 0.0), radius=0.2), density=1.0, groupIndex=1)
        id = self.gen_id('player')
        body = self.world.CreateDynamicBody(position=position, fixtures=fixtureDef, userData=Data(id=id, type='player', name=name), fixedRotation=True)
        self.childs[id] = body
        return id

    def add_wall(self, pos, rect):
        fixtureDef = b2FixtureDef(shape=b2PolygonShape(box=rect, pos=b2Vec2(0.0, 0.0)), density=0.0, groupIndex=-2)
        id = self.gen_id('wall')
        # self.wall_seed += 1
        body = self.world.CreateStaticBody(position=pos, fixtures=fixtureDef, userData=Data(id=id, type='wall'))
        # self.childs[id] = body
        return id

    def add_bullet(self, id, parent, dmg):
        pos = parent.position.copy()
        pos.x += (0.0055 + parent.fixtures[0].shape.radius) * math.cos(parent.angle)
        pos.y += (0.0055 + parent.fixtures[0].shape.radius) * math.sin(parent.angle)

        fixtureDef = b2FixtureDef(shape=b2CircleShape(pos=b2Vec2(0.0, 0.0), radius=0.004), density=0.0, groupIndex=-3)
        # bullet_id =  str(id) + '_' + str(time.time())
        bullet_id = self.gen_id('bullet')
        # self.bullet_seed += 1
        body = self.world.CreateDynamicBody(position=pos, bullet=True, fixtures=fixtureDef, angle=parent.angle, userData=Data(id=bullet_id, type='bullet', parent=parent, damage=dmg))
        v = b2Vec2(math.cos(body.angle), math.sin(body.angle))
        v *= bulletspeed
        body.linearVelocity = v
        self.childs[bullet_id] = body
        return bullet_id

    def add_spawn(self, pos, type):
        if type == 'player':
            id = self.gen_id('spawn')
            data = Data(id=id, type='spawn', position=pos)
            self.player_spawns.append(data)
            return id
        if type == 'item':
            pass
        pass


    def add_door(self, pos, rect, orientation):
        id = self.gen_id('door')
        # self.door_seed += 1
        fixtureDef = b2FixtureDef(shape=b2PolygonShape(box=rect, pos=b2Vec2(0.0, 0.0)), density=2.0, groupIndex=-2)
        body0 = self.world.CreateDynamicBody(position=pos, fixtures=fixtureDef, userData=Data(id=id, type='door'))

        if orientation == 0:#right
            pos = (pos[0] - rect[0] + rect[1], pos[1])
            # rect = (rect[1] / 2.0, rect[1] / 2.0)
        elif orientation == 2:#left
            pos = (pos[0] + rect[0] - rect[1], pos[1])
            # rect = (rect[1] / 2.0, rect[1] / 2.0)
        elif orientation == 1:#down
            pos = (pos[0], pos[1] + rect[0] - rect[1])
            # rect = (rect[0] / 2.0, rect[0] / 2.0)
        elif orientation == 3:#up
            pos = (pos[0], pos[1] - rect[0] + rect[1])
            # rect = (rect[0] / 2.0, rect[0] / 2.0)
        # fixtureDef = b2FixtureDef(shape=b2PolygonShape(box=rect, pos=b2Vec2(0.0, 0.0)), density=2.0, groupIndex=-2)
        # body1 = self.world.CreateBody(position=pos, fixtures=fixtureDef, userData=Data(id=id, type='door'))
        body1 = self.world.CreateBody(position=pos, userData=Data(id=id, type='door'))
        joint = self.world.CreateRevoluteJoint(bodyA=body0, bodyB=body1, anchor=body1.worldCenter, enableLimit=True, lowerAngle=math.pi*-0.5, upperAngle=math.pi*0.5)
        self.childs[id] = body0
        return id


    def killed(self, id, bullet_id):
        # print id
        print 'killed: ', id
        self.childs[bullet_id].userData.parent.userData.kills += 1
        self.del_child(id)
        # self.add_player(id, ((random.randint(0, 500) - 250)/200.0, (random.randint(0, 500) - 250)/200.0))
        self.spawn(id)

    def spawn(self, id):
        r = random.randint(0, len(self.player_spawns) - 1)

        self.add_player(id, self.player_spawns[r].position)

        pass

    def del_child(self, id):
        self.world.DestroyBody(self.childs.pop(id))
        self.ids.put(id)

    # a = 0

    def step(self):
        self.world.Step(self.timeStep, self.vel_iters, self.pos_iters)

        self.process_bullets()
        self.process_doors()

        self.world.contactListener.clear()
        self.world.ClearForces()
        # if World.a == 50:
        #     print self.world_state_deb()
        #     World.a = 0
        # else:
        #     World.a += 1

    def process_doors(self):
        for door in self.world.contactListener.doors:
            q = abs(door.userData.angle - door.angle)
            if q < 0.05:
                # door.userData.state = 0
                door.joints[0].joint.motorEnabled = False
                door.joints[0].joint.motorSpeed = 0
                door.angle = door.userData.angle
                door.angularVelocity = 0
                door.linearVelocity = (0, 0)
                door.fixedRotation = True
                door.userData.locked = False
                self.world.contactListener.doors.remove(door)

    def process_bullets(self):
        if self.world.contactListener.hits != []:
            for bullet, body in [(hit[0], hit[1]) for hit in self.world.contactListener.hits]:
                if body.userData.type == 0:
                    self.killed(body.userData.id, bullet.userData.id)
                elif 0:
                    pass

            for bullet in self.world.contactListener.bullets:
                self.del_child(bullet.userData.id)

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
        if id not in self.childs:
            return
        body = self.childs[id]
        v = b2Vec2(velocity)
        if body.fixtures[0].filterData.groupIndex == 1:
            v *= speed
        body.linearVelocity = v
        body.angle = angle
        if click:
            self.add_bullet(id, body, 0.0)

    def world_state(self):
        message = ''
        for key in self.childs:
            body = self.childs[key]
            message += '^' + str(key)
            message += '^' + str(body.userData.type)
            message += '^' + str(int(body.position.x * pixels_per_meter))
            message += '^' + str(int(body.position.y * pixels_per_meter))
            message += '^' + str(body.angle)
        return message

    def rad_to_deg(self, r):
        # if r < 0:
        #     r = b2_pi - r
        d = r * 180 / b2_pi
        return int(d)

    def deg_to_rad(self, d):
        r = d * b2_pi / 180
        return r

    # def world_state_ec(self, id):
    #     message = bytearray(len(self.childs) * 8)
    #     self.offset = 0
    #     for key in self.childs.keys():
    #         self.int_to_bytes(message, key)
    #     return message

    def world_state_ec(self, id):
        message = bytearray(len(self.childs) * 8)
        self.offset = 0
        self.int_to_bytes(message, id)
        visible = list(self.childs.keys())
        visible.remove(id)
        for key in visible:
            self.int_to_bytes(message, key)
        return message

    def int_to_bytes(self, blob, id):
        body = self.childs[id]
        i_h = body.userData.id
        x_h = int(body.position.x * pixels_per_meter)
        y_h = int(body.position.y * pixels_per_meter)
        a_h = self.rad_to_deg(body.angle)

        struct.pack_into('<h', blob, self.offset, i_h)
        struct.pack_into('<h', blob, self.offset + 2, x_h)
        struct.pack_into('<h', blob, self.offset + 4, y_h)
        struct.pack_into('<h', blob, self.offset + 6, a_h)

        deb = ''

        for i in range(self.offset, self.offset + 8):
            deb += str(blob[i]) + '\t'
        self.offset += 8
        # print deb
        return deb

    def world_state_deb(self):
        message = ''
        for key in self.childs:
            body = self.childs[key]
            message += str(key)
            # message += ' t:' + str(body.userData.type)
            message += ' x:' + str(int(body.position.x * pixels_per_meter))
            message += ' y:' + str(int(body.position.y * pixels_per_meter))
            message += ' a:' + str(self.rad_to_deg(body.angle)) + '\n'
        return message


class Data:

    types = {'player': 0,
             'wall': 1,
             'bullet': 2,
             'door': 3,
             'spawn': 4}

    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.type = Data.types.get(kwargs['type'])
        if self.type == 0:
            self.kills = 0
            self.name = kwargs['name']
        elif self.type == 2:
            self.hit = 0
            self.damage = kwargs['damage']
        elif self.type == 3:
            self.state = 0
            self.angle = 0
            self.locked = False
        elif self.type == 4:
            self.position = kwargs['position']

        if 'parent' in kwargs:
            self.parent = kwargs['parent']


class myContactListener(b2ContactListener):

    def __init__(self):
        b2ContactListener.__init__(self)
        # self.shot_points = []
        self.doors = []
        self.bullets = []
        self.hits = []

    def BeginContact(self, contact):
        # print 'begin contact'
        pass

    def EndContact(self, contact):
        # print 'end contact'
        pass

    def PreSolve(self, contact, oldManifold):
        bodyA = contact.fixtureA.body
        bodyB = contact.fixtureB.body
        # print 'pre-solve', bodyA.userData.id, bodyB.userData.id
        worldManifold = contact.worldManifold

        body = 0
        wall = 0
        bullet = 0
        door = 0
        type = bodyA.userData.type
        if type == 0:
            body = bodyA
        elif type == 1:
            wall = bodyA
        elif type == 2:
            bullet = bodyA
        elif type == 3:
            door = bodyA

        type = bodyB.userData.type

        if type == 0:
            body = bodyB
        elif type == 1:
            wall = bodyB
        elif type == 2:
            bullet = bodyB
        elif type == 3:
            door = bodyB

        b = False

        state1, state2 = b2GetPointStates(oldManifold, contact.manifold)

        # if state2[0] == b2_addState:
        if bullet != 0:
            contact.enabled = False
            # self.shot_points.append(contact)
            if wall != 0:
                self.hits.append((bullet, wall))
            elif body != 0:
                self.hits.append((bullet, body))
            elif door != 0:
                self.hits.append((bullet, door))
            if bullet not in self.bullets:
                self.bullets.append(bullet)
                # b = True
        if door != 0:
            self.processDoor(door, contact, worldManifold)

    def processDoor(self, door, contact, worldManifold):
            # print 'd'
            if contact.enabled:
                if not door.userData.locked:
                    print door.userData.id, 'go'
                    self.doors.append(door)
                    door.joints[0].joint.motorEnabled = True
                    door.joints[0].joint.maxMotorTorque  = 10
                    door.fixedRotation = False
                    door.userData.locked = True

                    if door.userData.state == 0:
                        d = self.direction(door, worldManifold.points[0])
                        print '0 to ' + str(d)
                        # if abs(d * math.pi / 2 + door.angle) <= math.pi / 2:
                        door.userData.state = d
                        door.userData.angle = d * math.pi / 2
                        door.joints[0].joint.motorSpeed = -d * math.pi
                    elif door.userData.state == 1:
                        print '1 to 0'
                        door.userData.state = 0
                        door.userData.angle = 0
                        door.joints[0].joint.motorSpeed = 1 * math.pi
                    elif door.userData.state == -1:
                        print '-1 to 0'
                        door.userData.state = 0
                        door.userData.angle = 0
                        door.joints[0].joint.motorSpeed = -1 * math.pi
                        door.fixedRotation = False

    def PostSolve(self, contact, impulse):
        pass

    def clear(self):
        self.bullets = []
        self.hits = []

    def direction(self, door, normal):
        c = door.joints[0].other.position
        a = door.position - c
        b = b2Vec2(normal) - c
        p = a.x * b.y - a.y * b.x
        if p > 0:
            return -1
        elif p < 0:
            return 1
        else:
            return 0