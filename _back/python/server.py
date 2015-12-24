from flask import Flask
from flask_sockets import Sockets
# from world import World, Body, Shape, Circle, Rectangle
from w2 import World
import random, time
import math
import threading
import gevent
import parser
import updater
from gevent import Greenlet

# sozdaem mir
world = World()
world.start()
# world.yaml = file('doc.yaml', 'r').read()
world.yaml = file('levels/big.yaml', 'r').read()
parser.parse(world, world.yaml)

# world.add_wall((-281.0/200.0, 0.0), (25/200.0, 306/200.0))
# world.add_wall((0.0, -281.0/200.0), (256/200.0, 25/200.0))
# world.add_wall((0.0, 281.0/200.0), (256/200.0, 25/200.0))
#
# world.add_wall((281.0/200.0, 178.0/200.0), (25/200.0, 128/200.0))
# world.add_wall((281.0/200.0, -178.0/200.0), (25/200.0, 128/200.0))
# world.add_door('door1', (281.0/200.0, 0.0/200.0), (5.0/200.0, 50.0/200.0), 3)



app = Flask(__name__)
sockets = Sockets(app)
updater_ = updater.Updater(world)
updater_.start()

i = 0
# client_sockets = {}


@sockets.route('/sock')
def echo_socket(ws):
    init_front(ws)



def init_front(ws):
    while not ws.closed:
        message = ws.receive()
        if message[0] == '#':
            id = message[1:]
            ws.send(world.yaml)
            print 'yaml sent', id
            wait_for_front_init(ws, id)
            break


def wait_for_front_init(ws, id):
    while not ws.closed:
        message = ws.receive()
        if message == 'ready':
            # p = ((random.randint(0, 500) - 250)/200.0, (random.randint(0, 500) - 250)/200.0)
            p = (0.0, 1.0) #sozdaem new body
            world.add_player(id, p)
            updater_.client_sockets[id] = ws
            print updater_.client_sockets.keys()
            print 'connected: ', id
            listen_socket(ws, id)
            break


def listen_socket(ws, id):
    while not ws.closed:
        # slushaem controlsy
        message = ws.receive()
        if message[0] == '*':
            control_body(message)
        elif message[0] == '~':
            id = message[1:]
            world.del_child(id)
            updater_.client_sockets.pop(id)
            print 'disconnected: ', id
            break



# @sockets.route('/connect')
# def echo_socket(ws):
#     qwe = 0;
#     ws.send('connect')
#     # gevent.sleep(5.0)
#     threading._sleep(5.0)
#     while True:
#         # message = ws.receive()
#         threading._sleep(1.0)
#         ws.send('ololo' + str(qwe))
#         qwe += 1


# def send_updates():
#     up = world.world_state()
#     # print up
#     for ws_id in client_sockets.keys():
#         try:
#             client_sockets.get(ws_id).send(up)
#         except Exception:
#             print '\n\ndisconnected!!!: ', ws_id
#             client_sockets.get(ws_id).close()
#             client_sockets.pop(ws_id)
#             world.del_child(ws_id)
#
#
# def start_updates():
#     while True:
#         gevent.spawn(send_updates)
#         gevent.sleep(0.02)

# tred na updeity clientam
# gevent.spawn(start_updates)

def control_body(message):
    # print message
    temp = message.split('*')
    id = temp[1]
    W = temp[2][0] == 't'
    S = temp[2][1] == 't'
    A = temp[2][2] == 't'
    D = temp[2][3] == 't'
    C = temp[2][4] == 't'
    # deg = -int(temp[2][5:])
    # angle1 = math.radians(deg)
    angle = -float(temp[2][5:])
    # print 'c', angle
    xmove = A * -1.0 + D * 1.0
    ymove = W * -1.0 + S * 1.0
    world.modify_child(id, [xmove/(math.sqrt(2), 1.0)[ymove == 0.0],
                            ymove/(math.sqrt(2), 1.0)[xmove == 0.0]], angle, C)


@app.route('/')
def hello_world():
    return 'Hello World!'
