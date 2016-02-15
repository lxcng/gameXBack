from w2 import *
import gevent
import random, time
import yaml
import parser

p = ((random.randint(0, 500) - 250)/200.0, (random.randint(0, 500) - 250)/200.0)

w = World()


w.yaml = file('levels/big.yaml', 'r').read()
parser.parse(w, w.yaml)

# w.add_player('112', (0.25, 0.0))
# w.add_player('112', (0.2, 0.35))
w.add_player('112', (150.0 / 200.0, -100.0 / 200.0))

# w.add_player('113', (0.85, 0.6))
# w.add_player('113', (0.85, 0.0))

# w.add_door('door1', (0.5, 0), (0.05, 0.4), 3)

# w.modify_child('112', (1.0, 0.0), 0, False)
w.modify_child('112', (0.0, 0.0), math.pi / 4, True)




for i in range(100):
    # w.modify_child('112', (-1.0, 0.0), 0, False)
    if i == 25:
        pass
    #     w.modify_child('113', (0.0, -1.0), 1.57, False)
    w.step()
    print i
    print w.world_state_deb()
    gevent.sleep(0.02)

