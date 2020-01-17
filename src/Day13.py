import matplotlib.pyplot as plt
import numpy as np
from src.lib.intcode import Amplifier


class Arcade:
	def __init__(self, verbose=False):
		self.board = {}
		self.score = 0
		self.ball = None
		self.paddle = None
		self.verbose = verbose

	def plot_game(self):
		colors = [0, 1, 2, 1, 3]
		r = np.zeros(max(self.board.keys()))
		for (pos_x, pos_y), c in self.board.items():
			r[pos_y, pos_x] = colors[c]
		plt.imshow(r)
		plt.show()

	def next_move(self):
		if self.verbose:
			print(f'## Ball at {self.ball}, paddle at {self.paddle}, returns {np.sign(self.ball[0] - self.paddle[0])}')
		return np.sign(self.ball[0] - self.paddle[0])


if __name__ == '__main__':
	with open('../inputs/Day13_input.txt', 'r') as f:
		program = list(map(int, f.read().strip().split(',')))

	outputs = []
	amp = Amplifier(program[:])
	arcade = Arcade()
	while not amp.done:
		x, y, tile_id = amp.run(), amp.run(), amp.run()
		arcade.board[(x, y)] = tile_id
	print(f"The result of first star is {sum(tile_id == 2 for tile_id in arcade.board.values())}.")

	program[0] = 2
	amp = Amplifier(program[:])
	arcade = Arcade()
	start_playing = False
	while not amp.done:
		if start_playing:
			amp.inputs = [arcade.next_move()]
		x, y, value = amp.run(), amp.run(), amp.run()
		if (x, y) == (-1, 0):
			arcade.score = value
			start_playing = True
			if arcade.verbose:
				print(f"Current score is {arcade.score}")
		else:
			if value == 4:
				arcade.ball = (x, y)
				if arcade.verbose:
					print(f"Ball is at {(x, y)}")
			elif value == 3:
				arcade.paddle = (x, y)
				if arcade.verbose:
					print(f"Paddle is at {(x, y)}")
			arcade.board[(x, y)] = value

	print(f'The result of second star is {arcade.score}.')