from flask import Flask
from flask_sockets import Sockets
from world import World, Body, Polygon
import random, time


world = World()
world.start();
# world.add_child(Body('bubiga', Polygon.circle([0,0], 1),[0,0]))

app = Flask(__name__)
sockets = Sockets(app)


@sockets.route('/connect')
def echo_socket(ws):
    while True:
        message = ws.receive()
        if message[0] == '#':
            id = message[1:]
            p = [random.randint(0, 500), random.randint(0, 500)]
            world.add_child(Body(id, Polygon.rectangle(p, 10, 10),p))
            # control_body(message)
            ws.send('ready')


@sockets.route('/control')
def echo_socket(ws):
    while True:
        message = ws.receive()
        if message[0] == '*':
            control_body(message)


@sockets.route('/update')
def echo_socket(ws):
    while True:
        ws.send(world.world_state())
        time.sleep(0.02)



def control_body(message):
    temp = message.split('*')
    id = temp[1]
    W = temp[2][0] == 't'
    S = temp[2][1] == 't'
    A = temp[2][2] == 't'
    D = temp[2][3] == 't'
    angle = float(temp[2][4:]) / 1000
    xmove = A * -1 + D * 1;
    ymove = W * -1 + S * 1;
    world.modify_child(id, [xmove, ymove], angle)


@app.route('/')
def hello_world():
    return 'Hello World!'
