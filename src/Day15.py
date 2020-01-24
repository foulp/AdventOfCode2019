import matplotlib.pyplot as plt
import numpy as np
from src.lib.intcode import Amplifier


class Droid:
	def __init__(self):
		self.map = {(0, 0): 2}
		self.pos = (0, 0)
		self.direction = 1
		self.shortest_path = {(0, 0): 0}
		self.oxygen = None
		self.cardinals = [1, 3, 2, 4]  # N, W, S, E

	def plot_game(self):
		min_x = min(v[0] for v in self.map.keys())
		min_y = min(v[1] for v in self.map.keys())
		size_x = max(v[0] for v in self.map.keys()) - min_x + 1
		size_y = max(v[1] for v in self.map.keys()) - min_y + 1
		r = 3 * np.ones((size_y, size_x))
		for (pos_x, pos_y), c in self.map.items():
			r[pos_y - min_y, pos_x - min_x] = c
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

	def explore_all_map(self, intcode):
		while self.pos != (0, 0) or self.oxygen is None:
			# We try to go right next
			next_d = self.cardinals[(self.cardinals.index(self.direction) + 1) % len(self.cardinals)]
			next_x, next_y = self.move(next_d)
			while (next_x, next_y) in self.map and self.map[(next_x, next_y)] == 0:
				# If already known, go straight, else go left, else go back
				next_d = self.cardinals[(self.cardinals.index(next_d) - 1) % len(self.cardinals)]
				next_x, next_y = self.move(next_d)

			case = intcode.run(next_d)
			if (next_x, next_y) != (0, 0):
				self.map[(next_x, next_y)] = case

			if case != 0:
				if (next_x, next_y) in self.shortest_path:
					self.shortest_path[(next_x, next_y)] = min(self.shortest_path[self.pos] + 1, self.shortest_path[(next_x, next_y)])
				else:
					self.shortest_path[(next_x, next_y)] = self.shortest_path[self.pos] + 1
				self.pos = (next_x, next_y)
				self.direction = next_d

			if case == 2:
				self.oxygen = (next_x, next_y)

		return

	def shortest_path_from_oxygen(self):
		compteur = 0
		oxygenized = {pos: 0 for pos in self.map if self.map[pos] != 0}
		oxygenized[self.oxygen] = 1
		current = [self.oxygen]
		while any((oxygenized[pos] == 0 for pos in oxygenized)):
			next_current = []
			for (x, y) in current:
				if self.map[(x+1, y)] != 0 and oxygenized[(x+1, y)] == 0:
					next_current.append((x+1, y))
					oxygenized[(x+1, y)] = 1
				if self.map[(x-1, y)] != 0 and oxygenized[(x-1, y)] == 0:
					next_current.append((x-1, y))
					oxygenized[(x-1, y)] = 1
				if self.map[(x, y-1)] != 0 and oxygenized[(x, y-1)] == 0:
					next_current.append((x, y-1))
					oxygenized[(x, y-1)] = 1
				if self.map[(x, y+1)] != 0 and oxygenized[(x, y+1)] == 0:
					next_current.append((x, y+1))
					oxygenized[(x, y+1)] = 1
			current = next_current[:]
			compteur += 1
		return compteur


if __name__ == '__main__':
	with open('../inputs/Day15_input.txt', 'r') as f:
		program = list(map(int, f.read().strip().split(',')))

	droid = Droid()
	amp = Amplifier(program)
	droid.explore_all_map(amp)
	# droid.plot_game()
	print(f"The result of first star is {droid.shortest_path[droid.oxygen]}")
	print(f"The result of second star is {droid.shortest_path_from_oxygen()}")
