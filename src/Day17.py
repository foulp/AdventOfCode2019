import numpy as np
from src.lib.intcode import Amplifier


class Scaffold:
	def __init__(self, intcode):
		self.amp = Amplifier(intcode)
		self.grid = self.construct_grid()
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
				if (self.grid[j, i-1:i+2] == ord('#')).all() and (self.grid[j-1:j+2, i] == ord('#')).all():
					self.alignment_parameter += i * j
		return self.alignment_parameter

	def find_path(self):
		path = []
		while True:
			x_l, y_l = self.turn('L')
			x_r, y_r = self.turn('R')
			if 0 <= x_l < self.grid.shape[0] and 0 <= y_l < self.grid.shape[1] and self.grid[x_l, y_l] == ord('#'):
				next_d = 'L'
			elif 0 <= x_r < self.grid.shape[0] and 0 <= y_r < self.grid.shape[1] and self.grid[x_r, y_r] == ord('#'):
				next_d = 'R'
			else:
				break

			path.append(next_d)
			self.direction = (self.direction+1 if next_d == 'R' else self.direction-1) % 4
			k = 0
			x_s, y_s = self.straight()
			while 0 <= x_s < self.grid.shape[0] and 0 <= y_s < self.grid.shape[1] and self.grid[x_s, y_s] == ord('#'):
				k += 1
				self.x, self.y = x_s, y_s
				x_s, y_s = self.straight()
			path.append(str(k))
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
		raise Exception(f"self.direction should be in [0-3], self.direction={self.direction}")

	def turn(self, direction):
		if (self.direction == 1 and direction == 'L') or (self.direction == 3 and direction == 'R'):
			return self.x-1, self.y
		if (self.direction == 0 and direction == 'R') or (self.direction == 2 and direction == 'L'):
			return self.x, self.y+1
		if (self.direction == 1 and direction == 'R') or (self.direction == 3 and direction == 'L'):
			return self.x+1, self.y
		if (self.direction == 0 and direction == 'L') or (self.direction == 2 and direction == 'R'):
			return self.x, self.y-1
		raise Exception(f"self.direction should be in [0-3] and direction in ['L', 'R'], "
						f"self.direction={self.direction} and direction={direction}")


def determine_functions(chemin):
	for i in range(2, len(chemin), 2):
		a = ''.join(chemin[:i])
		for j in range(2, len(chemin) - i, 2):
			b = ''.join(chemin[i: i+j])
			for k in range(2, len(chemin) - i - j, 2):
				c = ''.join(chemin[i+j: i+j+k])

				pass
	return path


def commands_to_ascii(function_commands):
	ascii_list = []
	for command in function_commands:
		ascii_list.append(list(map(ord, command+'\n')))
	return ascii_list


commands = ['A,A,B,C,B,C,B,C,A,C', 'R,6,L,8,R,8', 'R,4,R,6,R,6,R,4,R,4', 'L,8,R,6,L,10,L,10', 'n']

if __name__ == '__main__':
	with open('../inputs/Day17_input.txt', 'r') as f:
		program = list(map(int, f.read().strip().split(',')))

	scaffold = Scaffold(program[:])
	scaffold.calculate_alignment_parameter()
	print(f"The result of first star is {scaffold.alignment_parameter}")

	program[0] = 2
	scaffold = Scaffold(program[:])
	path = scaffold.find_path()
	message = ''
	inputs = commands_to_ascii(commands)
	while len(inputs):
		case = scaffold.amp.run()
		message += chr(case)
		if case == ord('\n'):
			print(message)
			message = chr(scaffold.amp.run(inputs.pop(0)))

	while not scaffold.amp.done:
		case = scaffold.amp.run()

	print(f"The result of second star is {case}")
