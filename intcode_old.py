# helper functions to handle intcode

from collections import defaultdict

def read_code(string):
    """
    string should be a comma-separated string.
    """

    code = defaultdict(int)
    for i, x in enumerate(string.split(',')):
        code[i] = int(x)
    return code

def read_code_old(string):
    return [int(x) for x in string.split(',')]

def get_value(code, mode, value, base=0):
    if mode == 0:
        # position mode
        return code[value]
    elif mode == 1:
        # immediate mode
        return value
    elif mode == 2:
        # relative mode
        return code[value + base]

def get_values(code, idx, params, base=0):
    return [
        get_value(code, param, code[idx+i], base=base)
        for i, param in enumerate(params, start=1)
    ]

def get_params(value, n_params):
    value = value // 100

    params = []
    for _ in range(n_params):
        params.append(int(value % 10))
        value //= 10
    
    return params

def run_program(code,
                inputs=None,
                print_outputs=True,
                halt_on_input=False,
                start_idx=0):
    idx = start_idx
    input_idx = 0
    base = 0
    outputs = []

    while True:
        # parse the value
        value = code[idx]
        opcode = value % 100

        # opcode, params = parse_value(code[idx])

        if opcode == 1:
            # Day 2
            params = get_params(value, 3)
            values = get_values(code, idx, params)
            code[code[idx+3]] = values[0] + values[1]

            idx += 4

        elif opcode == 2:
            # Day 2
            params = get_params(value, 3)
            values = get_values(code, idx, params)
            code[code[idx+3]] = values[0] * values[1]

            idx += 4

        elif opcode == 3:
            # Day 5
            if halt_on_input and (inputs is None or input_idx >= len(inputs)):
                return code, outputs, idx

            if inputs is None:
                input_val = int(input())
            else:
                input_val = inputs[input_idx]
                input_idx += 1
            code[code[idx+1]] = input_val

            idx += 2

        elif opcode == 4:
            # Day 5
            params = get_params(value, 1)
            v = get_value(code, params[0], code[idx+1])
            outputs.append(v)
            if print_outputs:
                print(v)

            idx += 2

        elif opcode == 5:
            # Day 5
            params = get_params(value, 2)
            values = get_values(code, idx, params)
            if values[0] != 0:
                idx = values[1]
            else:
                idx += 3

        elif opcode == 6:
            # Day 5
            params = get_params(value, 2)
            values = get_values(code, idx, params)
            if values[0] == 0:
                idx = values[1]
            else:
                idx += 3

        elif opcode == 7:
            # Day 5
            params = get_params(value, 3)
            values = get_values(code, idx, params)
            if values[0] < values[1]:
                code[code[idx+3]] = 1
            else:
                code[code[idx+3]] = 0

            idx += 4

        elif opcode == 8:
            # Day 5
            params = get_params(value, 3)
            values = get_values(code, idx, params)
            if values[0] == values[1]:
                code[code[idx+3]] = 1
            else:
                code[code[idx+3]] = 0

            idx += 4

        elif opcode == 9:
            # Day 9
            params = get_params(value, 1)
            values = get_values(code, idx, params)
            base += values[0]

            idx += 2

        elif opcode == 99:
            return code, outputs

        else:
            raise ValueError
