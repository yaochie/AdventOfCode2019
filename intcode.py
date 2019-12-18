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


class IntCode:
    def __init__(self, code):
        self.code = code
        self.base = 0

        # instruction pointer
        self.idx = 0
        self.terminated = False

    @staticmethod
    def load_code(code_string):
        return IntCode(read_code(code_string))

    @staticmethod
    def load_from_file(filename):
        return IntCode.load_code(open(filename, 'r').read())

    def copy(self):
        return IntCode(self.code)

    def get_value(self, mode, value):
        if mode == 0:
            # position mode
            return self.code[value]
        elif mode == 1:
            # immediate mode
            return value
        elif mode == 2:
            # relative mode
            return self.code[value + self.base]

    def get_values(self, params):
        return [
            self.get_value(param, self.code[self.idx + i])
            for i, param in enumerate(params, start=1)
        ]

    def get_params(self, value, n_params):
        value = value // 100

        params = []
        for _ in range(n_params):
            params.append(int(value % 10))
            value //= 10
        
        return params

    def run(self, inputs=None, print_outputs=True):
        input_idx = 0
        outputs = []

        while True:
            # parse the value
            value = self.code[self.idx]
            opcode = value % 100

            # opcode, params = parse_value(code[idx])

            if opcode == 1:
                # Day 2
                params = self.get_params(value, 3)
                values = self.get_values(params)
                self.code[self.code[self.idx+3]] = values[0] + values[1]

                self.idx += 4

            elif opcode == 2:
                # Day 2
                params = self.get_params(value, 3)
                values = self.get_values(params)
                self.code[self.code[self.idx+3]] = values[0] * values[1]

                self.idx += 4

            elif opcode == 3:
                # Day 5
                if inputs is None or input_idx >= len(inputs):
                    # halt if we are expecting an input, resume later
                    return outputs

                input_val = inputs[input_idx]
                input_idx += 1
                self.code[self.code[self.idx+1]] = input_val

                self.idx += 2

            elif opcode == 4:
                # Day 5
                params = self.get_params(value, 1)
                v = self.get_value(params[0], self.code[self.idx+1])
                outputs.append(v)
                if print_outputs:
                    print(v)

                self.idx += 2

            elif opcode == 5:
                # Day 5
                params = self.get_params(value, 2)
                values = self.get_values(params)
                if values[0] != 0:
                    self.idx = values[1]
                else:
                    self.idx += 3

            elif opcode == 6:
                # Day 5
                params = self.get_params(value, 2)
                values = self.get_values(params)
                if values[0] == 0:
                    self.idx = values[1]
                else:
                    self.idx += 3

            elif opcode == 7:
                # Day 5
                params = self.get_params(value, 3)
                values = self.get_values(params)
                if values[0] < values[1]:
                    self.code[self.code[self.idx+3]] = 1
                else:
                    self.code[self.code[self.idx+3]] = 0

                self.idx += 4

            elif opcode == 8:
                # Day 5
                params = self.get_params(value, 3)
                values = self.get_values(params)
                if values[0] == values[1]:
                    self.code[self.code[self.idx+3]] = 1
                else:
                    self.code[self.code[self.idx+3]] = 0

                self.idx += 4

            elif opcode == 9:
                # Day 9
                params = self.get_params(value, 1)
                values = self.get_values(params)
                self.base += values[0]

                self.idx += 2

            elif opcode == 99:
                self.terminated = True
                return outputs

            else:
                raise ValueError