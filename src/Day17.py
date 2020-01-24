import numpy as np
from src.lib.intcode import Amplifier


class VacuumRobot:
	def __init__(self, pos, direction):
		self.pos = pos
		self.direction = list(map(ord, ['^', 'v', '>', '<'])).index(direction)


class Scaffold:
	def __init__(self, intcode):
		self.program = intcode
		self.grid = self.construct_grid()
		x, y = np.where(np.isin(self.grid, list(map(ord, ['>', '>', 'v', '^']))))
		self.vacuumRobot = VacuumRobot((x[0], y[0]), self.grid[x, y])
		self.alignment_parameter = 0

	def construct_grid(self):
		grid = []
		line = []
		amp = Amplifier(self.program[:])
		while amp.done is False:
			case = amp.run()  # chr(amp.run())
			if case == ord('\n'):
				if len(line):
					grid.append(line[:])
				line = []
			else:
				line.append(case)
		return np.array(grid)

	def calculate_alignment_parameter(self):
		for j in range(1, self.grid.shape[0] - 1):
			for i in range(1, self.grid.shape[1] - 1):
				if (self.grid[j, i-1:i+2] == ord('#')).all() and (self.grid[j-1:j+2, i] == ord('#')).all():
					self.alignment_parameter += i * j
		return self.alignment_parameter


if __name__ == '__main__':
	with open('../inputs/Day17_input.txt', 'r') as f:
		program = list(map(int, f.read().strip().split(',')))

	scaffold = Scaffold(program[:])
	scaffold.calculate_alignment_parameter()
	print(f"The result of first star is {scaffold.alignment_parameter}")

	commands = 'R'
	program[0] = 2
	amp = Amplifier(program[:])
	print(f"The result of second star is {0}")
