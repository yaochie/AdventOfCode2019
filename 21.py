from intcode import IntCode, to_ascii

code = IntCode.load_from_file('../data/input21')

# Jump if the fourth tile is ground,
# and any of the previous three are not?
# (!A | !B | !C) & D
program = [
    "NOT A J",
    "NOT B T",
    "OR T J",
    "NOT C T",
    "OR T J",
    "AND D J",
    "WALK",
]

def make_program(prog):
    return [
        instr
        for line in program
        for instr in to_ascii(line)
    ]

inputs = make_program(program)
code1 = code.copy()
outputs = code1.run(inputs=inputs, print_outputs=False)

def draw_map(map):
    for value in map:
        print(chr(value), end='')

if outputs[-1] > 255:
    print(outputs[-1])
else:
    draw_map(outputs)

# part 2

# D & (!A | !B | !C) & (E | H)
# doesn't cover everything?, but good enough
program = [
    "NOT A J",
    "NOT B T",
    "OR T J",
    "NOT C T",
    "OR T J",
    "AND D J",
    "NOT H T",
    "NOT T T",
    "OR E T",
    "AND T J",
    "RUN",
]

inputs = make_program(program)
code2 = code.copy()
outputs = code2.run(inputs=inputs, print_outputs=False)

if outputs[-1] > 255:
    print(outputs[-1])
else:
    draw_map(outputs)