import yaml


def parse(w, n):
    f = yaml.load(n)
    walls = f['walls']
    for wall in walls:
        parse_wall(w, wall)

    doors = f['doors']
    for door in doors:
        parse_door(w, door)


def parse_wall(w, d):
    w.add_wall((d['x']/200.0, d['y']/200.0), (d['w']/200.0, d['h']/200.0))


def parse_door(w, d):
    w.add_door(d['id'], (d['x']/200.0, d['y']/200.0), (d['w']/200.0, d['h']/200.0), d['o'])

