from intcode import IntCode

orig_code = IntCode.load_from_file('../data/input11')

def update_direction(d, turn, curr_square):
    if turn == 0:
        d = (d - 1) % 4
    else:
        d = (d + 1) % 4

    if d == 0:
        curr_square = (curr_square[0]-1, curr_square[1])
    elif d == 1:
        curr_square = (curr_square[0], curr_square[1]-1)
    elif d == 2:
        curr_square = (curr_square[0]+1, curr_square[1])
    elif d == 3:
        curr_square = (curr_square[0], curr_square[1]+1)

    return d, curr_square

colors = {}
curr_square = (0, 0)
direction = 0

code = orig_code.copy()
while not code.terminated:
    # get color of current square
    inputs = [colors.get(curr_square, 0)]
    
    outputs = code.run(inputs=inputs, print_outputs=False)
    colors[curr_square] = outputs[0]

    # update location and direction
    direction, curr_square = update_direction(direction, outputs[1], curr_square)

print(len(colors))


# part 2
code = orig_code.copy()

curr_square = (0, 0)
colors = {curr_square: 1}
direction = 0

while not code.terminated:
    # get color of current square
    inputs = [colors.get(curr_square, 0)]
    
    outputs = code.run(inputs=inputs, print_outputs=False)
    colors[curr_square] = outputs[0]

    # update location and direction
    direction, curr_square = update_direction(direction, outputs[1], curr_square)

# draw panels
painted = list(colors.keys())
min_x = min(x[0] for x in painted)
max_x = max(x[0] for x in painted)
min_y = min(x[1] for x in painted)
max_y = max(x[1] for x in painted)

width = max_y - min_y + 1
height = max_x - min_x + 1

for i in range(height):
    row = []
    for j in range(width):
        loc = (min_x + i, max_y - j)
        if colors.get(loc, 0) == 0:
            print('.', end='')
        else:
            print('#', end='')
        
    print()
