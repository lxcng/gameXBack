from flask import Flask
from flask_sockets import Sockets
from world import World
import math
import lvlreader
from updater import Updater
import array
from sys import getsizeof


# sozdaem mir
world = World()
world.yaml = open('levels/big.yaml', 'r').read()
lvlreader.parse(world)
world.start()


app = Flask(__name__)
sockets = Sockets(app)
updater = Updater(world)
updater.start()

# client_sockets = {}


@sockets.route('/sock')
def echo_socket(ws):
    print('1')
    init_front(ws)


def init_front(ws):
    while not ws.closed:
        message = ws.receive()
        print ('m', message, type(message), len(message))
        print (int.from_bytes(message[:2], byteorder='big', signed=True))
        print (int.from_bytes(message[2:4], byteorder='big', signed=True))
        # print (int.from_bytes(message[:2], byteorder='big', signed=True))
        # print (int.from_bytes(message[:2], byteorder='big', signed=True))
        # print message, len(message), getsizeof(message)
        if message[0] == '#':
            id = message[1:]
            # ws.send(world.yaml)
            ws.send([elem.encode("hex") for elem in world.yaml])
            print ('yaml sent to: ', id)
            wait_for_front_init(ws, id)
            break


def wait_for_front_init(ws, id):
    while not ws.closed:
        message = ws.receive()
        print ('m', message)
        if message == 'ready':
            # p = ((random.randint(0, 500) - 250)/200.0, (random.randint(0, 500) - 250)/200.0)
            p = (0.0, 1.0) #sozdaem new body
            id = world.add_player(id, p)
            updater.client_sockets[id] = ws
            # print updater_.client_sockets.keys()
            print ('connected: ', id)
            listen_socket(ws, id)
            break


def listen_socket(ws, id):
    while not ws.closed:
        # slushaem controlsy
        message = ws.receive()
        # if message == None:
        #     continue
        # print 'c', message
        if message[0] == '*':
            pass
            control_body(id, message)
        elif message[0] == '~':
            # id = message[1:]
            world.del_child(id)
            updater.client_sockets.pop(id)
            print ('disconnected: ', id)
            break


def control_body(id, message):
    # print message
    # temp = message.split('*')
    # id = temp[1]
    W = message[1] == 't'
    S = message[2] == 't'
    A = message[3] == 't'
    D = message[4] == 't'
    C = message[5] == 't'
    # deg = -int(temp[2][5:])
    # angle1 = math.radians(deg)
    angle = -float(message[6:])
    # print 'c', angle
    xmove = A * -1.0 + D * 1.0
    ymove = W * -1.0 + S * 1.0
    world.modify_child(id, [xmove/(math.sqrt(2), 1.0)[ymove == 0.0],
                            ymove/(math.sqrt(2), 1.0)[xmove == 0.0]], world.deg_to_rad(angle), C)


@app.route('/')
def hello_world():
    s = '<!DOCTYPE HTML><html><head><title>Gunplay</title></style></head><body><p>Sockets</p>'
    for b in world.childs.values():
        if b.userData.type == 0:
            s += '<li>' + b.userData.id + ' :\t' + str(b.userData.kills) + '</li>'
    s += '</body></html>'
    print(s)
    return "Hello, world!"
    # return ''.format(s)


# @app.route('/')
# def hello_world():
#     s = ''
#     for b in world.childs.values():
#         if b.userData.type == 0:
#             s += b.userData.id + '\t' + str(b.userData.kills) + '\n'
#     print s
#     return '<!DOCTYPE HTML><html><head><title>Gunplay</title></style></head><body>{}</body></html>'.format(s)

# world.add_player('112', (0.25, 0.0))
# hello_world()