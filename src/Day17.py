import numpy as np
from src.lib.intcode import Amplifier


class Scaffold:
	def __init__(self, intcode):
		self.program = intcode
		self.grid = self.construct_grid()
		x, y = np.where(np.isin(self.grid, list(map(ord, ['^', 'v', '>', '<']))))
		self.x = x[0]
		self.y = y[0]
		self.direction = '^>v<'.index(chr(self.grid[x, y]))
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

	def find_path(self):
		path = ''
		while True:
			x_l, y_l = self.turn('L')
			if x_l < self.grid.shape[0] and y_l < self.grid.shape[1] and self.grid[x_l, y_l] == ord('#'):
				next_d = 'L'
			else:
				x_r, y_r = self.turn('R')
				if x_r < self.grid.shape[0] and y_r < self.grid.shape[1] and self.grid[x_r, y_r] == ord('#'):
					next_d = 'R'
				else:
					break

			path += next_d
			self.direction = (self.direction+1 if next_d == 'R' else self.direction-1) % 4
			k = 0
			while self.grid[self.straight()] == ord('#'):
				k += 1
				self.x, self.y = self.straight()
				if self.x == self.grid.shape[0]-1 or self.y == self.grid.shape[1]-1:
					break
			path += str(k)
		return path

	def straight(self):
		if self.direction == 0:
			return self.x-1, self.y
		if self.direction == 1:
			return self.x, self.y+1
		if self.direction == 2:
			return self.x+1, self.y
		if self.direction == 3:
			return self.x, self.y-1

	def turn(self, direction):
		if (self.direction == 1 and direction == 'L') or (self.direction == 3 and direction == 'R'):
			return self.x-1, self.y
		if (self.direction == 0 and direction == 'R') or (self.direction == 2 and direction == 'L'):
			return self.x, self.y+1
		if (self.direction == 1 and direction == 'R') or (self.direction == 3 and direction == 'L'):
			return self.x+1, self.y
		if (self.direction == 0 and direction == 'L') or (self.direction == 2 and direction == 'R'):
			return self.x, self.y-1


if __name__ == '__main__':
	with open('../inputs/Day17_input.txt', 'r') as f:
		program = list(map(int, f.read().strip().split(',')))

	scaffold = Scaffold(program[:])
	scaffold.calculate_alignment_parameter()
	print(f"The result of first star is {scaffold.alignment_parameter}")

	print(scaffold.find_path())
	program[0] = 2
	scaffold = Scaffold(program[:])
	print(f"The result of second star is {0}")
