from itertools import product

def trace_wire(moves):
    loc = (0, 0)
    trace = [loc]
    dist = [0]
    for move in moves:
        d, steps = move[0], int(move[1:])

        if d == 'L':
            loc = (loc[0]+steps, loc[1])
        elif d == 'R':
            loc = (loc[0]-steps, loc[1])
        elif d == 'U':
            loc = (loc[0], loc[1]+steps)
        elif d == 'D':
            loc = (loc[0], loc[1]-steps)
        else:
            raise ValueError

        trace.append(loc)
        dist.append(dist[-1] + steps)

    return trace, dist

def intersect(seg1, seg2):
    # seg1 is vertical
    return not (
        seg1[0][0] > max(seg2[0][0], seg2[1][0]) or
        seg1[0][0] < min(seg2[0][0], seg2[1][0]) or
        seg2[0][1] > max(seg1[0][1], seg1[1][1]) or
        seg2[0][1] < min(seg1[0][1], seg1[1][1])
    )

def find_intersections(trace1, trace2):
    segments1 = list(zip(trace1[:-1], trace1[1:]))
    segments2 = list(zip(trace2[:-1], trace2[1:]))

    intersections = []
    int_idxes = []

    for (i, seg1), (j, seg2) in product(enumerate(segments1), enumerate(segments2)):
        if seg1[0][0] != seg1[1][0]:
            seg1, seg2 = seg2, seg1

        # seg1 is vertical (seg1[0][0] == seg1[1][0])
        if intersect(seg1, seg2):
            intersections.append((seg1[0][0], seg2[0][1]))
            int_idxes.append((i, j))

    return intersections, int_idxes

def manhattan_distance(loc):
    return sum(map(abs, loc))

def find_dist(c1, c2):
    a, b = c1
    x, y = c2
    assert (a == x) or (b == y)

    return abs(a - x) + abs(b - y)

wire1, wire2 = open('../data/input3').readlines()

wire1, steps1 = trace_wire(wire1.split(','))
wire2, steps2 = trace_wire(wire2.split(','))

intersections, int_idxes = find_intersections(wire1, wire2)

ans1 = min(
    filter(lambda x: x > 0,
        map(manhattan_distance, intersections)
    )
)
print(ans1)

min_dist = None
for inter, (i, j) in zip(intersections, int_idxes):
    dist1 = steps1[i] + find_dist(wire1[i], inter)
    dist2 = steps2[j] + find_dist(wire2[j], inter)

    if dist1 + dist2 == 0:
        continue

    min_dist = dist1 + dist2 if min_dist is None else min(min_dist, dist1 + dist2)

print(min_dist)
