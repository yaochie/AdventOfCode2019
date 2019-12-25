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


def to_ascii(line):
    """
    Writes a string as ASCII code. Appends a newline at the end.
    """
    data = [ord(c) for c in line]
    data.append(10)
    return data


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
        """
        Returns a fresh copy of the code, **in the same state**.
        """
        return IntCode(self.code.copy())

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

    def get_values(self, modes):
        return [
            self.get_value(mode, self.code[self.idx + i])
            for i, mode in enumerate(modes, start=1)
        ]

    def get_modes(self, value, n_modes):
        value = value // 100

        modes = []
        for _ in range(n_modes):
            modes.append(int(value % 10))
            value //= 10
        
        return modes

    def write_to(self, mode, param, value):
        """
        write value to the location given by param, based on the mode.
        """
        if mode == 0:
            # position mode
            self.code[param] = value
        elif mode == 1:
            # cannot be in immediate mode
            raise ValueError
        elif mode == 2:
            # relative mode
            self.code[param + self.base] = value

    def run(self, inputs=None, print_outputs=True):
        """
        Resumes the code from the current instruction, using the
        given 'inputs' for any required inputs.

        When it halts, the outputs from this run are returned.

        If the program has terminated, the 'terminated' flag is set.
        """
        input_idx = 0
        outputs = []

        while True:
            # parse the value
            value = self.code[self.idx]
            opcode = value % 100

            if opcode == 1:
                # Day 2
                modes = self.get_modes(value, 3)
                values = self.get_values(modes)
                self.write_to(modes[2], self.code[self.idx+3], values[0] + values[1])

                self.idx += 4

            elif opcode == 2:
                # Day 2
                modes = self.get_modes(value, 3)
                values = self.get_values(modes)
                self.write_to(modes[2], self.code[self.idx+3], values[0] * values[1])

                self.idx += 4

            elif opcode == 3:
                # Day 5
                if inputs is None or input_idx >= len(inputs):
                    # halt if we are expecting an input, resume later
                    return outputs

                input_val = inputs[input_idx]
                input_idx += 1

                modes = self.get_modes(value, 1)
                self.write_to(modes[0], self.code[self.idx+1], input_val)

                self.idx += 2

            elif opcode == 4:
                # Day 5
                modes = self.get_modes(value, 1)
                v = self.get_value(modes[0], self.code[self.idx+1])
                outputs.append(v)
                if print_outputs:
                    print(v)

                self.idx += 2

            elif opcode == 5:
                # Day 5
                modes = self.get_modes(value, 2)
                values = self.get_values(modes)
                if values[0] != 0:
                    self.idx = values[1]
                else:
                    self.idx += 3

            elif opcode == 6:
                # Day 5
                modes = self.get_modes(value, 2)
                values = self.get_values(modes)
                if values[0] == 0:
                    self.idx = values[1]
                else:
                    self.idx += 3

            elif opcode == 7:
                # Day 5
                modes = self.get_modes(value, 3)
                values = self.get_values(modes)

                compare_val = 1 if values[0] < values[1] else 0
                self.write_to(modes[2], self.code[self.idx+3], compare_val)

                self.idx += 4

            elif opcode == 8:
                # Day 5
                modes = self.get_modes(value, 3)
                values = self.get_values(modes)

                compare_val = 1 if values[0] == values[1] else 0
                self.write_to(modes[2], self.code[self.idx+3], compare_val)

                self.idx += 4

            elif opcode == 9:
                # Day 9
                modes = self.get_modes(value, 1)
                values = self.get_values(modes)
                self.base += values[0]

                self.idx += 2

            elif opcode == 99:
                self.terminated = True
                return outputs

            else:
                raise ValueError