__author__ = 'alex'
from world import World, Body, Polygon
import matplotlib.pyplot as plt
import math
import numpy as np


a = World(1)
# b = Body(2)

c = Polygon.circle((0, 0), 5)
r = Polygon.rectangle((5,10), 5,5)


# for i in range(12):
plt.xlim(-3, 3)
plt.ylim(-3, 3)
for i in range(12):
    q = Polygon((0.0, 0.0), np.array([[2.0, 0.0]]))
    q.rotate((i /6.0)*math.pi)
    v = q.vertices
    plt.text(v[0, 0], v[0, 1], i, fontsize=15)
    plt.scatter(v[:, 0], v[:, 1])
plt.show()
# print a.arg + b.arg