from world import World, Body, Shape, Circle, Rectangle
# from world import World, Body, Polygon
import threading
import time
# import matplotlib.pyplot as plt
import traceback

a = World()
# a.add_child(Body('wall_l', Rectangle([-271.0, 0.0], 50, 612), [-271.0, 0.0], 'wall'))
# a.add_child(Body('wall_r', Rectangle([271.0, 0.0], 50, 612), [271.0, 0.0], 'wall'))
# a.add_child(Body('wall_u', Rectangle([0.0, -271.0], 512, 50), [0.0, -271.0], 'wall'))
# a.add_child(Body('wall_b', Rectangle([0.0, 271.0], 512, 50), [0.0, 271.0], 'wall'))


# w =  Rectangle([3, 0], 2, 4)
# print isinstance(w, Rectangle)

# a.add_child(Body('2', Circle([0,0], 1),[0,0],'s'))
# a.add_child(Body('3', Circle([0,0], 1),[0,0],'s'))
# a.add_child(Body('4', Circle([0,0], 1),[0,0],'s'))
# a.add_child(Body('5', Circle([0,0], 1),[0,0],'s'))
# a.add_child(Body('6', Rectangle([0,0], 1, 3),[0,0],'s'))
a.add_child(Body('7', Rectangle([0, 0], 1, 5), [0, 0], 'pl'))
#
# a.modify_child('1', [0.5, 0.0], 0.0, False)
# a.step()
a.add_child(Body('1', Circle([0, 0], 1), [0, 0], 'pl'))
a.add_child(Body('wall_1', Rectangle([8, 0], 6, 6), [8, 0], 'wall'))
a.modify_child('1', [0.0, 0.0], 0.0, True)

# while True:
#     a.step()
start = time.time()
a.step()
print 'step', time.time() - start