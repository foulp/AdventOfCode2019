import numpy as np
from src.lib.intcode import Amplifier


class Scaffold:
    def __init__(self, intcode):
        self.amp = Amplifier(intcode)
        self.grid = self.construct_grid()
        self.path = []
        self.main = []
        self.functions = []
        x, y = np.where(np.isin(self.grid, list(map(ord, ['^', 'v', '>', '<']))))
        self.x = x[0]
        self.y = y[0]
        self.direction = '^>v<'.index(chr(self.grid[x, y]))
        self.alignment_parameter = 0

    def construct_grid(self):
        grid = []
        line = []
        while self.amp.done is False:
            case = self.amp.run()
            if case == ord('\n'):
                if len(grid) == 0 or len(line) == len(grid[0]):
                    grid.append(line[:])
                    line = []
                else:
                    break
            else:
                line.append(case)
        return np.array(grid)

    def calculate_alignment_parameter(self):
        for j in range(1, self.grid.shape[0] - 1):
            for i in range(1, self.grid.shape[1] - 1):
                if (self.grid[j, i - 1:i + 2] == ord('#')).all() and (self.grid[j - 1:j + 2, i] == ord('#')).all():
                    self.alignment_parameter += i * j
        return self.alignment_parameter

    def find_path(self):
        while True:
            x_l, y_l = self.turn('L')
            x_r, y_r = self.turn('R')
            if 0 <= x_l < self.grid.shape[0] and 0 <= y_l < self.grid.shape[1] and self.grid[x_l, y_l] == ord('#'):
                next_d = 'L'
            elif 0 <= x_r < self.grid.shape[0] and 0 <= y_r < self.grid.shape[1] and self.grid[x_r, y_r] == ord('#'):
                next_d = 'R'
            else:
                break

            self.path.append(next_d)
            self.direction = (self.direction + 1 if next_d == 'R' else self.direction - 1) % 4
            k = 0
            x_s, y_s = self.straight()
            while 0 <= x_s < self.grid.shape[0] and 0 <= y_s < self.grid.shape[1] and self.grid[x_s, y_s] == ord('#'):
                k += 1
                self.x, self.y = x_s, y_s
                x_s, y_s = self.straight()
            self.path.append(str(k))

    def straight(self):
        if self.direction == 0:
            return self.x - 1, self.y
        if self.direction == 1:
            return self.x, self.y + 1
        if self.direction == 2:
            return self.x + 1, self.y
        if self.direction == 3:
            return self.x, self.y - 1
        raise Exception(f"self.direction should be in [0-3], self.direction={self.direction}")

    def turn(self, direction):
        if (self.direction == 1 and direction == 'L') or (self.direction == 3 and direction == 'R'):
            return self.x - 1, self.y
        if (self.direction == 0 and direction == 'R') or (self.direction == 2 and direction == 'L'):
            return self.x, self.y + 1
        if (self.direction == 1 and direction == 'R') or (self.direction == 3 and direction == 'L'):
            return self.x + 1, self.y
        if (self.direction == 0 and direction == 'L') or (self.direction == 2 and direction == 'R'):
            return self.x, self.y - 1
        raise Exception(
            f"self.direction should be in [0-3] and direction in ['L', 'R'], "
            f"self.direction={self.direction} and direction={direction}")

    def determine_functions(self, chemin, n=3):
        if len(self.functions) == n:
            return len(chemin) == 0

        k = len(self.main)
        for i in range(2, min(len(chemin) + 2, 22), 2):
            self.functions.append(chemin[:i])
            self.main.append('ABC'[len(self.functions) - 1])
            chemin_cut = chemin[i:]
            while any(chemin_cut[:len(pattern)] == pattern for pattern in self.functions):
                for j, pattern in enumerate(self.functions):
                    if ''.join(chemin_cut).startswith(''.join(pattern)):
                        chemin_cut = chemin_cut[len(pattern):]
                        self.main.append('ABC'[j])
            if self.determine_functions(chemin_cut):
                return True
            else:
                self.functions.pop()
                self.main = self.main[:k]
        return False


def commands_to_ascii(function_commands):
    ascii_list = []
    for command in function_commands:
        ascii_list.append(list(map(ord, command + '\n')))
    return ascii_list


if __name__ == '__main__':
    with open('../inputs/Day17_input.txt', 'r') as f:
        program = list(map(int, f.read().strip().split(',')))

    scaffold = Scaffold(program[:])
    scaffold.calculate_alignment_parameter()
    print(f"The result of first star is {scaffold.alignment_parameter}")

    program[0] = 2
    scaffold = Scaffold(program[:])
    scaffold.find_path()
    scaffold.determine_functions(scaffold.path)
    message = ''
    inputs = commands_to_ascii([','.join(scaffold.main)] + [','.join(v) for v in scaffold.functions] + ['n'])
    while len(inputs):
        out_case = scaffold.amp.run()
        message += chr(out_case)
        if out_case == ord('\n'):
            print(message)
            message = chr(scaffold.amp.run(inputs.pop(0)))

    out_case = 0
    while not scaffold.amp.done:
        out_case = scaffold.amp.run()

    print(f"The result of second star is {out_case}")
