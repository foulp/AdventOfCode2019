import matplotlib.pyplot as plt
import numpy as np
import random
from src.Day13 import Arcade
from src.lib.intcode import Amplifier


class Droid:
	def __init__(self):
		self.map = {(0, 0): 2}
		self.pos = (0, 0)
		self.oxygen = None

	def plot_game(self):
		colors = [0, 1, 2]
		min_x = min(v[0] for v in self.map.keys())
		min_y = min(v[1] for v in self.map.keys())
		size_x = max(v[0] for v in self.map.keys()) - min_x + 1
		size_y = max(v[1] for v in self.map.keys()) - min_y + 1
		r = 3 * np.ones((size_x, size_y))
		for (pos_x, pos_y), c in self.map.items():
			r[pos_x + min_x, pos_y + min_y] = colors[c]
		plt.imshow(r)
		plt.show()

	def move(self, n):
		if n == 1:
			return self.pos[0], self.pos[1] + 1
		if n == 2:
			return self.pos[0], self.pos[1] - 1
		if n == 3:
			return self.pos[0] + 1, self.pos[1]
		if n == 4:
			return self.pos[0] - 1, self.pos[1]
		raise ValueError(f"direction should be in [1, 2, 3, 4], it was {n}.")

	def shortest_path(self):
		xs, ys = 0, 0
		xo, yo = self.oxygen
		return 0


if __name__ == '__main__':
	with open('../inputs/Day15_input.txt', 'r') as f:
		program = list(map(int, f.read().strip().split(',')))

	droid = Droid()
	amp = Amplifier(program)
	while droid.oxygen is None:
		candidates = [i for i in range(1, 5) if droid.move(i) not in droid.map.keys()]
		if len(candidates):
			direction = random.choice(candidates)
		else:
			direction = random.choice([i for i in range(1, 5) if droid.map[droid.move(i)] != 0])

		x, y = droid.move(direction)
		location = amp.run(direction)
		droid.map[(x, y)] = location
		if location != 0:
			droid.pos = (x, y)
		if location == 2:
			droid.oxygen = (x, y)

	droid.plot_game()

	print(f"The result of first star is {droid.shortest_path()}")
