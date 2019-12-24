from collections import deque

from intcode import IntCode

next_direction = {
    1: 4,
    2: 3,
    3: 1,
    4: 2,
}
prev_direction = {
    1: 3,
    2: 4,
    3: 2,
    4: 1,
}

def next_loc(loc, direction):
    if direction == 1:
        return (loc[0], loc[1]+1)
    elif direction == 2:
        return (loc[0], loc[1]-1)
    elif direction == 3:
        return (loc[0]+1, loc[1])
    elif direction == 4:
        return (loc[0]-1, loc[1])

def draw(world, location):
    min_x = min(x[0] for x in world.keys())
    min_y = min(x[1] for x in world.keys())
    max_x = max(x[0] for x in world.keys())
    max_y = max(x[1] for x in world.keys())

    for i in range(min_x, max_x+1):
        for j in range(min_y, max_y+1):
            if (i, j) == location:
                char = 'D'
            elif (i, j) == (0, 0):
                char = 'S'
            elif (i, j) not in world:
                char = ' '
            elif world[(i, j)] == 0:
                char = '#'
            elif world[(i, j)] == 1:
                char = '.'
            elif world[(i, j)] == 2:
                char = '*'

            print(char, end='')
        print()

code = IntCode.load_from_file('../data/input15')

world = {}

location = (0, 0)
oxygen = None
world[location] = 1

direction = 1
while not code.terminated:
    # follow the wall
    outputs = code.run(inputs=[direction], print_outputs=False)

    next_location = next_loc(location, direction)
    world[next_location] = outputs[0]

    if outputs[0] == 0:
        direction = next_direction[direction]
    elif outputs[0] == 1:
        location = next_location
        direction = prev_direction[direction]
    elif outputs[0] == 2:
        # found oxygen!
        location = next_location
        direction = prev_direction[direction]
        oxygen = location
        print(f"Oxygen is at {oxygen}")

    if next_location == (0, 0):
        # reached the start, terminate
        break

print(code.terminated)

draw(world, location)

def bfs(start_node, oxygen=True):
    queue = deque([start_node])

    # mapping from location to distance
    node = start_node
    visited = {node: 0}

    done = False
    while len(queue) > 0 and not done:
        node = queue.popleft()
        curr_dist = visited[node]
        for d in [1, 2, 3, 4]:
            next_node = next_loc(node, d)

            if next_node in world and next_node not in visited:
                if oxygen and world[next_node] == 2:
                    # done!
                    print("Ans 1:", curr_dist + 1)
                    done = True
                    break

                if world[next_node] == 0:
                    continue

                visited[next_node] = curr_dist + 1
                queue.append(next_node)

    if not oxygen:
        print("Ans 2:", max(visited.values()))

bfs((0, 0), oxygen=True)

# part 2
# bfs from the oxygen system to all nodes

bfs(oxygen, oxygen=False)