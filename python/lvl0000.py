from world import World, Body, Polygon
import threading
import time
import matplotlib.pyplot as plt
import traceback

a = World()
a.add_child(Body('1', Polygon.circle([0,0], 1),[0,0]))
a.add_child(Body('2', Polygon.circle([0,0], 1),[0,0]))
a.add_child(Body('3', Polygon.circle([0,0], 1),[0,0]))
a.add_child(Body('4', Polygon.circle([0,0], 1),[0,0]))
a.add_child(Body('5', Polygon.circle([0,0], 1),[0,0]))

a.del_child('3')
# a.childs['1'].velocity = [0.01, 0.0]
# a.modify_child('1', (0.01, 0.0), 1)

# print a.world_state()
i = 0
calls = 0

def tred():
    global i, calls
    if calls < 5:
        threading.Timer(0.02, tred).start()
        calls += 1
    # a.step()
    calls -= 1
    print i, time.time(), a.childs['1'].position
    # i += 1
# plt.xlim(-3, 3)
# plt.ylim(-3, 3)
# plt.scatter(a.childs['1'].shape.vertices[:, 0], a.childs['1'].shape.vertices[:, 1])
# plt.show()
tred()
a.start()
a.modify_child('1', (0.0, 0.01), 1)
# plt.scatter(a.childs['1'].shape.vertices[:, 0], a.childs['1'].shape.vertices[:, 1])
# plt.show()
# a.modify_child('1', (0.01, 0.0), 2)
# plt.scatter(a.childs['1'].shape.vertices[:, 0], a.childs['1'].shape.vertices[:, 1])
# plt.show()
# a.modify_child('1', (0.0, 0.01), 3)
# plt.scatter(a.childs['1'].shape.vertices[:, 0], a.childs['1'].shape.vertices[:, 1])
# plt.show()
# time.sleep(1)
# for line in traceback.format_stack():
#         print line.strip()

