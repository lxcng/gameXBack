import gevent


class Updater:

    def __init__(self, world):
        self.client_sockets = {}
        self.world = world
        self.delay = world.timeStep
        self.running = False

    def add_client(self, id, ws):
        self.client_sockets[id] = ws

    def send_updates(self):
        up = self.world.world_state()
        for ws_id in self.client_sockets.keys():
            try:
                self.client_sockets.get(ws_id).send(up)
                # print 'up', ws_id
            except Exception:
                print '\n\ndisconnected!!!: ', ws_id
                self.client_sockets.get(ws_id).close()
                self.client_sockets.pop(ws_id)
                self.world.del_child(ws_id)

    def start_updates(self):
        while self.running:
            gevent.spawn(self.send_updates)
            gevent.sleep(self.delay)

    def start(self):
        self.running = True
        gevent.spawn(self.start_updates)
        print 'updates started', self.delay

    def stop(self):
        self.running = False