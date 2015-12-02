from flask import Flask
from flask_sockets import Sockets
# from world import World, Body, Shape, Circle, Rectangle
from w2 import World
import random, time
import math
import threading
import gevent
from gevent import Greenlet

# sozdaem mir
world = World()
world.start()
world.add_wall((-281.0/200.0, 0.0), (25/200.0, 306/200.0))
world.add_wall((0.0, -281.0/200.0), (256/200.0, 25/200.0))
world.add_wall((0.0, 281.0/200.0), (256/200.0, 25/200.0))

world.add_wall((281.0/200.0, 178.0/200.0), (25/200.0, 128/200.0))
world.add_wall((281.0/200.0, -178.0/200.0), (25/200.0, 128/200.0))
world.add_door('door1', (281.0/200.0, 5.0/200.0), (5.0/200.0, 45.0/200.0), 3)



app = Flask(__name__)
sockets = Sockets(app)
i = 0
client_sockets = {}


@sockets.route('/sock')
def echo_socket(ws):
    global i

    # jdem I message ot clienta
    while True:
        message = ws.receive()
        if message[0] == '#':
            id = message[1:]
            # p = [random.randint(0, 500), random.randint(0, 500)]
            p = (0.0, 0.0) #sozdaem new body
            world.add_player(id, p)
            client_sockets[id] = ws
            ws.send('ready')
            break

    while True:
        # slushaem controlsy
        message = ws.receive()
        if message[0] == '*':
            control_body(message)
        elif message[0] == '~':
            id = message[1:]
            world.del_child(id)
            client_sockets.pop(id)
            break



@sockets.route('/connect')
def echo_socket(ws):
    qwe = 0;
    ws.send('connect')
    # gevent.sleep(5.0)
    threading._sleep(5.0)
    while True:
        # message = ws.receive()
        threading._sleep(1.0)
        ws.send('ololo' + str(qwe))
        qwe += 1


def send_updates():
    up = world.world_state()
    for ws in client_sockets.keys():
        try:
            client_sockets.get(ws).send(up)
        except Exception:
            client_sockets.get(ws).close()
            client_sockets.pop(ws)


def start_updates():
    while True:
        gevent.spawn(send_updates)
        gevent.sleep(0.02)

# tred na updeity clientam
gevent.spawn(start_updates)

def control_body(message):
    # print message
    temp = message.split('*')
    id = temp[1]
    W = temp[2][0] == 't'
    S = temp[2][1] == 't'
    A = temp[2][2] == 't'
    D = temp[2][3] == 't'
    C = temp[2][4] == 't'
    # angle = math.radians(-int(temp[2][5:]))
    angle = -float(temp[2][5:])
    xmove = A * -1.0 + D * 1.0
    ymove = W * -1.0 + S * 1.0
    world.modify_child(id, [xmove/(math.sqrt(2), 1.0)[ymove == 0.0],
                            ymove/(math.sqrt(2), 1.0)[xmove == 0.0]], angle, C)


@app.route('/')
def hello_world():
    return 'Hello World!'
