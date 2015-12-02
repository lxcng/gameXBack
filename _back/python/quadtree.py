
import math

class Quadtree:

    capacity = 3
    depth = 10

    def __init__(self, lvl, rect):
        self.level = lvl
        self.bounds = rect
        self.nodes = []
        self.objects = []

    def clear(self):
        del self.objects[:]
        while len(self.nodes) != 0:
            self.nodes.pop().clear()

    def split(self):
        x = self.bounds[0]
        y = self.bounds[1]
        subw = self.bounds[2]/2
        subh = self.bounds[3]/2
        self.nodes.append(Quadtree(self.level + 1, (x, y, subw, subh)))
        self.nodes.append(Quadtree(self.level + 1, (x + subw, y, subw, subh)))
        self.nodes.append(Quadtree(self.level + 1, (x, y + subh, subw, subh)))
        self.nodes.append(Quadtree(self.level + 1, (x + subw, y + subh, subw, subh)))

    inds = [[[0], [0, 2], [2]],
            [[0, 1], [0, 1, 2, 3], [2, 3]],
            [[1], [1, 3], [3]]]

    def get_index(self, obj):
        index = -1
        midx = self.bounds[0] + self.bounds[2] / 2
        midy = self.bounds[1] + self.bounds[3] / 2

        xl = obj.shape.bounds[0] - midx
        xu = obj.shape.bounds[0] + obj.shape.bounds[2] - midx
        yl = obj.shape.bounds[1] - midy
        yu = obj.shape.bounds[1] + obj.shape.bounds[3] - midy
        x = -1
        y = -1
        if xl * xu >= 0:
            if xl > 0:
                x = 2
            else:
                x = 0
        else:
            x = 1
        if yl * yu >= 0:
            if yl > 0:
                y = 2
            else:
                y = 0
        else:
            y = 1
        return Quadtree.inds[x][y]

    def insert(self, obj):
        if len(self.nodes) != 0:
            index = self.get_index(obj)
            if index != -1:
                for i in index:
                    self.nodes[i].insert(obj)
                return

        self.objects.append(obj)

        if len(self.objects) > Quadtree.capacity and self.level < Quadtree.depth:
            if len(self.nodes) == 0:
                self.split()
            for o in self.objects:
                index = self.get_index(o)
                if index != -1:
                    for i in index:
                        self.nodes[i].insert(o)

    def retrieve(self, obj):
        index = self.get_index(obj)
        if index != -1 and len(self.nodes) != 0:
            res = []
            for i in index:
                res += self.nodes[i].retrieve(obj)
            res = list(set(res))
            # try:
            #     res.remove(obj)
            # except Exception:
            #     pass
            return res

        return self.objects


class Ob:
    def __init__(self, x, y):
        self.shape = Q(x,y)

class Q:
    def __init__(self, x,y):
        self.bounds = [x, y, 10, 10]

q = Quadtree(0, [0, 0, 1000, 1000])

o1 = Ob(10, 260)
o2 = Ob(260, 260)
o3 = Ob(260, 10)
o4 = Ob(245, 10)
q.insert(o1)
q.insert(o2)
q.insert(o3)
q.insert(Ob(10, 10))
q.insert(o4)
w = q.retrieve(o4)
pass
# q.clear()












