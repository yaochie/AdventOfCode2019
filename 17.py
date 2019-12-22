from intcode import IntCode

def draw_camera(camera_output):
    for value in camera_output:
        print(chr(value), end='')

def camera_to_array(camera_output):
    arr = []
    row = []
    for value in camera_output:
        if value == 10:
            if len(row) > 0:
                arr.append(row)
                row = []
        else:
            row.append(value)

    print(len(arr), len(arr[0]))    

    return arr

def get_param_sum(camera_data):
    param_sum = 0
    for i, row in enumerate(camera_data[:-1]):
        for j, value in enumerate(row[:-1]):
            if i == 0 or j == 0:
                continue

            hash_val = ord('#')
            if value != hash_val:
                continue

            neighbours = [
                camera_data[i-1][j],
                camera_data[i+1][j],
                camera_data[i][j-1],
                camera_data[i][j+1],
            ]
            if all(n == hash_val for n in neighbours):
                # print("Intersection at", i, j)
                param_sum += i * j

    return param_sum

code = IntCode.load_from_file('../data/input17')

outputs = code.run(print_outputs=False)

print(code.terminated)

# draw_camera(outputs)
camera_data = camera_to_array(outputs)
print("Ans 1:", get_param_sum(camera_data))

# data = """..#..........
# ..#..........
# #######...###
# #.#...#...#.#
# #############
# ..#...#...#..
# ..#####...^..""".splitlines()

# data = [
#     [ord(char) for char in line]
#     for line in data
# ]
# print(get_param_sum(data))


# part 2

print("-------------")
print("part 2")
print("-------------")

code = IntCode.load_from_file('../data/input17')

code.code[0] = 2

sequence = ','.join(c for c in 'ABACBCBCAC')
funcs = [
    'L,10,R,12,R,12',
    'R,6,R,10,L,10',
    'R,10,L,10,L,12,R,6'
]

def to_ascii(line):
    data = [ord(c) for c in line]
    data.append(10)
    return data

# print(sequence)

# while True:
#     outputs = code.run(inputs=[], print_outputs=False)
#     draw_camera(outputs)
#     break

code_inputs = []
code_inputs.extend(to_ascii(sequence))
code_inputs.extend(to_ascii(funcs[0]))
code_inputs.extend(to_ascii(funcs[1]))
code_inputs.extend(to_ascii(funcs[2]))
code_inputs.extend(to_ascii('n'))

outputs = code.run(inputs=code_inputs, print_outputs=False)
# print(outputs[-1])

draw_camera(outputs[:-1])
print(code.terminated)
print(outputs[-1])