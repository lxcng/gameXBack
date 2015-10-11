__author__ = 'alex'
from world import World, Body, Polygon
# import matplotlib.pyplot as plt
import math
import numpy as np
from flask import Flask
from flask_sockets import Sockets
from world import World, Body, Polygon
import random, time
import math
import threading
import gevent


i = 0

def w(a):
    print a


def qwerty():
    global i
    while True:
        gevent.spawn(w, 'qwerty' + str(i))
        i += 1
        gevent.sleep(0.02)

gevent.spawn(qwerty)
print '1'
gevent.sleep(5.0)