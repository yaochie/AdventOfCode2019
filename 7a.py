from itertools import permutations

from intcode import IntCode

code = IntCode.load_from_file('../data/input7')

# part 1
max_signal = 0
for phases in permutations(range(5)):
    outputs = [0]
    for phase in phases:
        outputs = code.copy().run(inputs=([phase] + outputs), print_outputs=False)

    max_signal = max(max_signal, outputs[0])

print(max_signal)


# part 2
max_signal = 0

for phases in permutations(range(5, 10)):
    codes = [code.copy() for _ in range(5)]

    # initialize programs with phase settings
    for code, phase in zip(codes, phases):
        code.run(inputs=[phase], print_outputs=False)

    # run the feedback loop
    inputs = [0]

    while not codes[-1].terminated:
        for code in codes:
            outputs = code.run(inputs=inputs, print_outputs=False)
            inputs = outputs

    max_signal = max(max_signal, outputs[0])

print(max_signal)