from w2 import *
import gevent


w = World()

w.add_player('112', (0.0, 0.0))
# w.add_wall((5, 0.0), (0.5, 10.0))

# w.modify_child('112', (1.0, 0.0), 0.0, False)


# print w.world_state()
# w.start()
w.add_door('door1', (0.5, 0), (0.05, 0.4), 1)
w.modify_child('112', (1.0, 0.0), 0, False)
# print w.childs['112'].userData.id
# print w.world_state()
for i in range(100):
    # if i == 5:
    #     w.modify_child('112', (1.0, 0.0), 1.57, True)
    w.step()
    print w.world_state()
    gevent.sleep(0.02)

    # print len(w.childs)
    # print i, '\t', w.childs['112'].linearVelocity.x, w.childs['112'].linearVelocity.y #, w.childs['112'].angle
    # print i, '\t', w.childs['door1'].angularVelocity
pass
pass