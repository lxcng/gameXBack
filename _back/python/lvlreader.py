import yaml


def parse(world):
    f = yaml.load(world.yaml)
    walls = f['walls']
    for wall in walls:
        parse_wall(world, wall)

    doors = f['doors']
    for door in doors:
        parse_door(world, door)

    spawns = f['spawns']
    for spawn in spawns:
        parse_spawns(world, spawn)

    world.yaml = yaml.dump(f)


def parse_wall(w, d):
    d['id'] = w.add_wall((d['x']/200.0, d['y']/200.0), (d['w']/200.0, d['h']/200.0))


def parse_door(w, d):
    d['id'] = w.add_door((d['x']/200.0, d['y']/200.0), (d['w']/200.0, d['h']/200.0), d['o'])


def parse_spawns(w, d):
    d['id'] = w.add_spawn((d['x']/200.0, d['y']/200.0), 'player')

