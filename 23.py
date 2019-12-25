from intcode import IntCode

code = IntCode.load_from_file('../data/input23')

n_computers = 50

computers = [
    code.copy()
    for _ in range(n_computers)
]

# initialize computers
all_outputs = []
for i, com in enumerate(computers):
    outputs = com.run(inputs=[i])
    all_outputs.append(outputs)

inputs = [[] for _ in range(n_computers)]

for output in all_outputs:
    if len(output) > 0:
        i = 0
        while i < len(output):
            dest, x, y = output[i:i+3]
            inputs[dest].append((x, y))
            i += 3

print("initialized")

# simulate
done = False
while not done:
    all_outputs = []
    for i, com in enumerate(computers):
        com_inputs = inputs[i]
        if len(com_inputs) == 0:
            com_inputs = [-1]
        else:
            com_inputs = [a for pair in com_inputs for a in pair]

        outputs = com.run(inputs=com_inputs)
        all_outputs.append(outputs)

    inputs = [[] for _ in range(n_computers)]
    for output in all_outputs:
        if len(output) == 0:
            continue

        i = 0
        while i < len(output):
            dest, x, y = output[i:i+3]

            # part 1
            if dest == 255:
                print("Ans 1:", y)
                done = True
                break

            inputs[dest].append((x, y))
            i += 3


# part 2

computers = [
    code.copy()
    for _ in range(n_computers)
]

# initialize computers
all_outputs = []
for i, com in enumerate(computers):
    outputs = com.run(inputs=[i])
    all_outputs.append(outputs)

inputs = [[] for _ in range(n_computers)]

for output in all_outputs:
    if len(output) > 0:
        i = 0
        while i < len(output):
            dest, x, y = output[i:i+3]
            inputs[dest].append((x, y))
            i += 3

print("initialized")

# simulate
nat_value = None
prev_blank = False
prev_y_nat = None
done = False
while not done:
    all_outputs = []
    for i, com in enumerate(computers):
        com_inputs = inputs[i]
        if len(com_inputs) == 0:
            com_inputs = [-1]
        else:
            com_inputs = [a for pair in com_inputs for a in pair]

        outputs = com.run(inputs=com_inputs)
        all_outputs.append(outputs)

    inputs = [[] for _ in range(n_computers)]

    if sum(len(outputs) for outputs in all_outputs) == 0:
        if prev_blank:
            # idle
            # print("idle!")
            assert nat_value is not None
            inputs[0].append(nat_value)

            if prev_y_nat is not None and nat_value[-1] == prev_y_nat:
                # part 2
                print("Ans 2:", prev_y_nat)
                done = True

            # nat_value = None
            prev_blank = False
            prev_y_nat = nat_value[-1]

        else:
            prev_blank = True
    else:
        prev_blank = False
        for output in all_outputs:
            if len(output) == 0:
                continue

            i = 0
            while i < len(output):
                dest, x, y = output[i:i+3]

                if dest == 255:
                    nat_value = (x, y)
                else:
                    inputs[dest].append((x, y))
                i += 3

    # print(all_outputs)
    # print(inputs)