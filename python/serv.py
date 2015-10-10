from flask import Flask
from flask_sockets import Sockets
from world import World, Body, Polygon
import random, time
import math
import threading


world = World()
world.start();
# world.add_child(Body('bubiga', Polygon.circle([0,0], 1),[0,0]))

app = Flask(__name__)
sockets = Sockets(app)
i = 0


@sockets.route('/sock')
def echo_socket(ws):
    global i
    while True:
        # ws.send(world.world_state())
        if i < 3:
            threading.Timer(ws.send(world.world_state()), 0.02).start()
            i += 1
        else:
            i -= 1
        message = ws.receive()

        if message[0] == '*':
            control_body(message)
        elif message[0] == '#':
            id = message[1:]
            # p = [random.randint(0, 500), random.randint(0, 500)]
            p = [0.0, 0.0]
            world.add_child(Body(id, Polygon.rectangle(p, 10, 10), p))
            ws.send('ready')
        elif message[0] == '~':
            id = message[1:]
            world.del_child(id)



# @sockets.route('/connect')
# def echo_socket(ws):
#     while True:
#         message = ws.receive()
#         if message[0] == '#':
#             id = message[1:]
#             p = [random.randint(0, 500), random.randint(0, 500)]
#             world.add_child(Body(id, Polygon.rectangle(p, 10, 10),p))
#             # control_body(message)
#             ws.send('ready')

#
# @sockets.route('/control')
# def echo_socket(ws):
#     while True:
#         message = ws.receive()


# @sockets.route('/update')
# def echo_socket(ws):
#     while True:
#         time.sleep(0.02)



def control_body(message):
    temp = message.split('*')
    id = temp[1]
    W = temp[2][0] == 't'
    S = temp[2][1] == 't'
    A = temp[2][2] == 't'
    D = temp[2][3] == 't'
    angle = float(temp[2][4:]) / 1000
    xmove = A * -1.0 + D * 1.0
    ymove = W * -1.0 + S * 1.0
    # xmove / (math.sqrt(2), 1.0) [ymove == 0.0]
    world.modify_child(id, [xmove/ (math.sqrt(2), 1.0) [ymove == 0.0],
                            ymove/ (math.sqrt(2), 1.0) [xmove == 0.0]], angle)


@app.route('/')
def hello_world():
    return 'Hello World!'
