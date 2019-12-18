from itertools import product

from intcode import IntCode

def init_code(code, noun, verb):
    code.code[1] = noun
    code.code[2] = verb
    return code

def try_prog(noun, verb):
    code = IntCode.load_code(open('../data/input2').read())
    code = init_code(code, noun, verb)

    _ = code.run()

    return code.code[0]

ans1 = try_prog(12, 2)
print(ans1)

for i, j in product(range(100), range(100)):
    ans = try_prog(i, j)
    if ans == 19690720:
        print(i*100 + j)
        break