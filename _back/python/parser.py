import yaml


def parse(world, n):
    f = yaml.load(n)
    walls = f['walls']
    for wall in walls:
        parse_wall(world, wall)

    doors = f['doors']
    for door in doors:
        parse_door(world, door)


def parse_wall(w, d):
    w.add_wall((d['x']/200.0, d['y']/200.0), (d['w']/200.0, d['h']/200.0))


def parse_door(w, d):
    w.add_door(d['id'], (d['x']/200.0, d['y']/200.0), (d['w']/200.0, d['h']/200.0), d['o'])

