from flask import Flask
from flask_sockets import Sockets
import time

# start_time = time.time()
# time.time() - start_time)
x = 250
y = 250
W = False
S = False
A = False
D = False
angle = 0.0
sq2 = 1.41421356237

app = Flask(__name__)
sockets = Sockets(app)


@sockets.route('/echo')
def echo_socket(ws):
    global W, S, A, D, angle
    while True:
        message = ws.receive()
        if message[0] == '*':
            W = message[1] == 't'
            S = message[2] == 't'
            A = message[3] == 't'
            D = message[4] == 't'
            angle = float(message[5:10]) / 1000
            step()
            ws.send("#" + str(x) + "#" + str(y) + "#" + message[5:10])

            # ws.send(message + 's')


def step():
    global x, y
    xmove = A * -1 + D * 1;
    ymove = W * -1 + S * 1;
    dx = 10 * xmove / (sq2, 1)[ymove == 0]
    dy = 10 * ymove / (sq2, 1)[xmove == 0]
    x += int(dx)
    y += int(dy)


@app.route('/')
def hello_world():
    return 'Hello World!'
