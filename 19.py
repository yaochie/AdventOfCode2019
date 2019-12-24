import itertools
import math

from intcode import IntCode

def draw_map(map):
    for row in map:
        for value in row:
            if value == 0:
                print('.', end='')
            else:
                print('#', end='')
        print()

def draw_map_dict(map):
    max_x = max(x[0] for x in map.keys())
    max_y = max(x[1] for x in map.keys())

    for x in range(max_x):
        for y in range(max_y):
            if (x, y) not in map:
                char = ' '
            else:
                char = '#' if map[(x, y)] == 1 else '.'
            
            print(char, end='')
        print()

def find_angle_limits(locs):
    max_angle = min_angle = math.atan2(1, 1)

    for x, y in locs:
        if x == 0 and y == 0:
            continue
        angle = math.atan2(x, y)
        max_angle = max(max_angle, angle)
        min_angle = min(min_angle, angle)

    print("Max:", max_angle)
    print("Min:", min_angle)

code = IntCode.load_from_file('../data/input19')

# part 1

def part1():
    affected_locs = []
    map = []
    for x in range(50):
        row = []
        for y in range(50):
            outputs = code.copy().run(inputs=[x, y], print_outputs=False)
            if outputs[0] == 1:
                affected_locs.append((x, y))

            row.extend(outputs)
        map.append(row)

        # if x % 5 == 0:
        #     find_angle_limits(affected_locs)

    n_affected = len(affected_locs)
    print("Ans 1:", n_affected)

    # draw_map(map)

    find_angle_limits(affected_locs)

# part1()
# sys.exit()

# part 2
# this method is quite slow (1-2 minutes, but it works),
# as we go from the first rows

# faster alternative would be to estimate the angle, and jump
# near to the correct rows

limit = 500
diff = 100
max_y = {}
min_y = 0
# affected = []
map = {}
for x in range(limit):
    if x in [1, 2, 3]:
        continue
    # row_affected = []

    found_row = False
    for y in range(min_y, limit):
        outputs = code.copy().run(inputs=[x, y], print_outputs=False)
        map[(x, y)] = outputs[0]
        if outputs[0] == 1:
            # row_affected.append((x, y))

            if not found_row:
                found_row = True
                min_y = y

                if x >= diff + 3 and x - diff + 1 in max_y:
                    if max_y[x - diff + 1] - min_y + 1 >= diff:
                        print()
                        print("Ans 2:", (x - diff + 1) * 10000 + y)
                        sys.exit()
        elif found_row: # outputs[0] == 0
            max_y[x] = y - 1
            break

    # affected.append(row_affected)

    if x >= 100:
        pass

    if x % 50 == 0:
        print(x, end='..', flush=True)

# draw_map_dict(map)

# # calculate angles of limits
# min_angle = math.atan2(1, 1)
# max_angle = math.atan2(1, 1)
# for x in range(5, limit):
#     ys = [p[1] for p in filter(lambda p: p[0] == x, map.keys())]
#     min_y, max_y = min(ys), max(ys)

#     # print(x, min_y, max_y)

#     if max_y < limit - 1:
#         min_angle = math.atan2(x, min_y)
#         max_angle = math.atan2(x, max_y)
#         print(x, min_angle, max_angle)
