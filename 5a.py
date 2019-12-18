from intcode import IntCode

print('----------\npart1\n-----------')
code = IntCode.load_code(open('../data/input5').read())
#code = read_code(open('../data/input5').read())
code.run(inputs=[1])
#run_program(code)

print('----------\npart2\n-----------')
# code = read_code(open('../data/input5').read())
# run_program(code)
code = IntCode.load_code(open('../data/input5').read())
code.run(inputs=[5])