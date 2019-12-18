from itertools import permutations, product
from intcode_old import read_code, run_program

code = read_code(open('../data/input7').read())

# code = read_code("3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0")
# code = read_code("3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0")
# code = read_code("3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0")

# part 1

max_signal = 0
for phases in permutations(range(5)):
    outputs = [0]
    for phase in phases:
        _, outputs = run_program(code.copy(), inputs=[phase, outputs[0]], print_outputs=False)

    max_signal = max(max_signal, outputs[0])

print(max_signal)

# # alternative for part 1
# max_signal = 0
# for phases in permutations(range(5)):
#     codes = [code.copy() for _ in range(5)]
#     idxes = [0 for _ in range(5)]
#     results = [None for _ in range(5)]

#     for i in range(5):
#         result = run_program(codes[i], inputs=[phases[i]],
#                             print_outputs=False, halt_on_input=True)

#         assert len(result) == 3
#         codes[i], _, idxes[i] = result

#         results[i] = result

#     prog_inputs = [None for _ in range(5)]
#     prog_inputs[0] = [0]

#     for i in range(5):
#         result = run_program(codes[i], inputs=prog_inputs[i],
#                             print_outputs=False, halt_on_input=True,
#                             start_idx=idxes[i])

#         assert len(result) == 2
#         _, prog_inputs[(i+1) % 5] = result

#         results[i] = result

#     max_signal = max(max_signal, results[-1][1][0])

# print(max_signal)

# part 2
max_signal = 0

#code = read_code("3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5")
#code = read_code("3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10")

for phases in permutations(range(5, 10)):
    codes = [code.copy() for _ in range(5)]
    idxes = [0 for _ in range(5)]
    results = [None for _ in range(5)]

    for i in range(5):
        result = run_program(codes[i], inputs=[phases[i]],
                            print_outputs=False, halt_on_input=True)

        assert len(result) == 3
        codes[i], _, idxes[i] = result

        results[i] = result

    prog_inputs = [None for _ in range(5)]
    prog_inputs[0] = [0]

    while len(results[-1]) == 3:
        for i in range(5):
            result = run_program(codes[i], inputs=prog_inputs[i],
                                print_outputs=False, halt_on_input=True,
                                start_idx=idxes[i])
            if len(result) == 2:
                _, prog_inputs[(i+1) % 5] = result
            elif len(result) == 3:
                codes[i], prog_inputs[(i+1) % 5], idxes[i] = result
            else:
                raise ValueError

            results[i] = result

    max_signal = max(max_signal, results[-1][1][0])

print(max_signal)