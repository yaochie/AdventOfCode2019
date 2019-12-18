from intcode import IntCode

code = IntCode.load_from_file('../data/input9')

# part 1
code.copy().run(inputs=[1])

# part 2
code.copy().run(inputs=[2])