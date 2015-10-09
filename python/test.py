__author__ = 'alex'
from world import World, Body, Polygon
import matplotlib.pyplot as plt
import math
import numpy as np



# plt.xlim(-3, 3)
# plt.ylim(-3, 3)
# for i in range(12):
#     q = Polygon((0.0, 0.0), np.array([[2.0, 0.0]]))
#     q.rotate((i /6.0)*math.pi)
#     v = q.vertices
#     plt.text(v[0, 0], v[0, 1], i, fontsize=15)
#

# a = World()
# a.add_child(Body('1', Polygon.circle([0,0], 1),[0,0]))
# a.childs['1'].velocity = [0.5, 0.5]
#
# for i in range(10):
#     a.step()
#     print a.childs['1'].position
#     plt.scatter(a.childs['1'].shape.vertices[:, 0], a.childs['1'].shape.vertices[:, 1])
#     plt.show()

from serv import control_body

control_body('*bubiga*tfff1234')