from collections import namedtuple
import copy

data = open('../data/input12').readlines()

# data = """<x=-1, y=0, z=2>
# <x=2, y=-10, z=-7>
# <x=4, y=-8, z=8>
# <x=3, y=5, z=-1>""".splitlines()

# data = """<x=-8, y=-10, z=0>
# <x=5, y=5, z=10>
# <x=2, y=-7, z=3>
# <x=9, y=-8, z=-3>""".splitlines()

def center_of_mass(positions):
    center = [0, 0, 0]
    for pos in positions:
        for k, c in enumerate(pos):
            center[k] += c

    for k, c in enumerate(center):
        center[k] /= len(positions)

    return center

def simulate(start_pos, start_vel, timesteps=None, check_repeat=False):
    positions = copy.deepcopy(start_pos)
    velocities = copy.deepcopy(start_vel)

    n = 0
    while timesteps is None or n < timesteps:
        n += 1
        # calculate velocity updates
        for i, pos1 in enumerate(positions):
            vel_update = [0] * len(pos1)
            for j, pos2 in enumerate(positions):
                if i == j:
                    continue
                
                for k, (c1, c2) in enumerate(zip(pos1, pos2)):
                    if c1 < c2:
                        vel_update[k] += 1
                    elif c1 > c2:
                        vel_update[k] -= 1

            # update velocity
            for k, c_update in enumerate(vel_update):
                velocities[i][k] += c_update

        # apply velocity
        for i, vel in enumerate(velocities):
            for k, c_update in enumerate(vel):
                positions[i][k] += c_update

        if check_repeat:
            if positions == start_pos and velocities == start_vel:
                print()
                print(n)
                return n
            if n % 10000 == 0:
                print(n, end='..', flush=True)

    return positions, velocities

def energy(pos, vel, com=[0, 0, 0]):
    pot_e = sum(abs(x - com[k]) for k, x in enumerate(pos))
    kin_e = sum(abs(x) for x in vel)
    return pot_e * kin_e

def system_energy(all_pos, all_vel, from_com=False):
    if from_com:
        com = center_of_mass(all_pos)
        return sum(energy(pos, vel, com=com) for pos, vel in zip(all_pos, all_vel))
    else:
        return sum(energy(pos, vel) for pos, vel in zip(all_pos, all_vel))

velocities = [[0, 0, 0] for _ in range(4)]

positions = []
for line in data:
    line = line.strip()[1:-1]
    x, y, z = line.split(', ')
    x = int(x[2:])
    y = int(y[2:])
    z = int(z[2:])

    positions.append([x, y, z])

# simulate
new_pos, new_vel = simulate(positions, velocities, 1000)
print(system_energy(new_pos, new_vel))

# part 2

# calculate periods for each coordinate? since they are all independent
periods = []
for i in range(3):
    sub_pos = [[pos[i]] for pos in positions]
    sub_vel = [[vel[i]] for vel in velocities]

    # print(sub_pos)
    period = simulate(sub_pos, sub_vel, check_repeat=True)
    periods.append(period)

def gcd_iter(a, b):
    # euclidean algorithm, iterative
    if a == b:
        return a

    if a < b:
        a, b = b, a

    c = (a - b) % b
    while b % c != 0:
        a, b = b, c
        c = (a - b) % b

    return c

def lcm(a, b):
    print(f"gcd of {a}, {b} =", gcd_iter(a, b))
    return a // gcd_iter(a, b) * b

def lcm_many(values):
    # from wiki, but quite slow
    x_0 = values.copy()
    x = values.copy()

    while sum(v - min(x) for v in x) > 0:
        to_update = min(x)
        for i, v in enumerate(x):
            if v == to_update:
                x[i] += x_0[i]
                break

    return x[0]

print(lcm(periods[0], lcm(periods[1], periods[2])))