from flask import Flask
from flask_sockets import Sockets
from w2 import World
import math
import parser
from updater import Updater


# sozdaem mir
world = World()
world.start()
world.yaml = file('levels/big.yaml', 'r').read()
parser.parse(world, world.yaml)


app = Flask(__name__)
sockets = Sockets(app)
updater = Updater(world)
updater.start()

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
            print 'yaml sent to: ', id
            wait_for_front_init(ws, id)
            break


def wait_for_front_init(ws, id):
    while not ws.closed:
        message = ws.receive()
        if message == 'ready':
            # p = ((random.randint(0, 500) - 250)/200.0, (random.randint(0, 500) - 250)/200.0)
            p = (0.0, 1.0) #sozdaem new body
            world.add_player(id, p)
            updater.client_sockets[id] = ws
            # print updater_.client_sockets.keys()
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
            updater.client_sockets.pop(id)
            print 'disconnected: ', id
            break


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
    s = ''
    for b in world.childs.values():
        if b.userData.type == 0:
            s += b.userData.id + '\t' + str(b.userData.kills) + '\n'
    print s
    return '<!DOCTYPE HTML><html><head><title>Gunplay</title></style></head><body>{}</body></html>'.format(s)
    # return '<!DOCTYPE HTML><html><head><title>Gunplay</title></style></head><body>{}</body></html>'.format(updater_.client_sockets.keys())

# world.add_player('112', (0.25, 0.0))
# hello_world()