# brute force? O(n^3)

import math
from operator import itemgetter
from itertools import zip_longest
from collections import defaultdict
from pprint import pprint

asteroids = []

data = open('../data/input10').readlines()
# data = """.#..##.###...#######
# ##.############..##.
# .#.######.########.#
# .###.#######.####.#.
# #####.##.#.##.###.##
# ..#####..#.#########
# ####################
# #.####....###.#.#.##
# ##.#################
# #####.##.###..####..
# ..######..##.#######
# ####.##.####...##..#
# .#####..#.######.###
# ##...#.##########...
# #.##########.#######
# .####.#.###.###.#.##
# ....##.##.###..#####
# .#.#.###########.###
# #.#.#.#####.####.###
# ###.##.####.##.#..##""".splitlines()

# data = """......#.#.
# #..#.#....
# ..#######.
# .#.#.###..
# .#..#.....
# ..#....#.#
# #..#....#.
# .##.#..###
# ##...#..#.
# .#....####""".splitlines()

for i, line in enumerate(data):
    for j, char in enumerate(line.strip()):
        if char == '#':
            asteroids.append((i, j))

print(asteroids)

# print(asteroids)
print("# asteroids:", len(asteroids))

def part1():
    ep = 1e-5

    max_detected = 0
    best_loc = None
    for i, (x, y) in enumerate(asteroids):
        print(i, end='..', flush=True)
        seen = set()
        for j, (a, b) in enumerate(asteroids):
            if i == j: continue

            # angle = math.atan2(a - x, b - y)
            angle = float("{:.5f}".format(math.atan2(a - x, b - y)))

            # check if blocked by currently seen asteroid
            blocked = False
            for (c, d) in seen:
                # angle2 = math.atan2(c - x, d - y)
                angle2 = float("{:.5f}".format(math.atan2(c - x, d - y)))
                if abs(angle2 - angle) < ep or abs(angle2 - angle - 2*math.pi) < ep:
                    if a < c:
                        seen.remove((c, d))
                        seen.add((a, b))

                    blocked = True
                    break

            if not blocked:
                seen.add((a, b))

        # print(seen)
        if len(seen) > max_detected:
            max_detected = len(seen)
            best_loc = (x, y)

    print()
    print(best_loc)
    print(max_detected)

# part1()

# part 2
location = (28, 29)

# calculate all angles and distances
angles = {}
dist_sq = {}
a, b = location
for (x, y) in asteroids:
    if location == (x, y): continue

    # hack to make sure we start from the asteroid to our north
    angle = math.atan2(x - a, y - b)
    if angle < -math.pi / 2:
        angle += 2 * math.pi
    # angles[(x, y)] = float("{:.5f}".format(math.atan2(x - a, y - b)))
    angles[(x, y)] = float(f"{angle:.5f}")
    dist_sq[(x, y)] = (x - a) ** 2 + (y - b) ** 2

# group asteroids by angle, then sort by distance
to_destroy = [
    (loc, angles[loc], dist_sq[loc])
    for loc in asteroids
    if loc != location
]

angle_lists = defaultdict(list)
for l, a, d in to_destroy:
    angle_lists[a].append((l, d))

for a, p in angle_lists.items():
    angle_lists[a] = sorted(p, key=itemgetter(1))

# pprint(angle_lists)
# convert to list, then use zip_longest
angle_lists = [
    angle_lists[a]
    for a in sorted(angle_lists.keys())
]

# get 200th in sequence
count = 0
for destroyed in zip_longest(*angle_lists, fillvalue=None):
    ds = list(filter(lambda x: x is not None, destroyed))
    if len(ds) + count < 200:
        count += len(ds)
        continue

    print(ds[200 - count - 1])
