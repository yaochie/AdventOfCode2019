from itertools import product

from intcode_old import read_code, run_program

def init_code(code, noun, verb):
    code[1] = noun
    code[2] = verb
    return code

def try_prog(noun, verb):
    code = read_code(open('../data/input2').read())
    code = init_code(code, noun, verb)
    return run_program(code)[0][0]

ans1 = try_prog(12, 2)
print(ans1)

for i, j in product(range(100), range(100)):
    ans = try_prog(i, j)
    if ans == 19690720:
        print(i*100 + j)
        break