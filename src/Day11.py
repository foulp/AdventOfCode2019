import matplotlib.pyplot as plt
import numpy as np
from src.lib.intcode import Amplifier


class EmergencyHullPainting:
	def __init__(self, intcode, starting_panel):
		self.program = intcode
		self.starting_panel = starting_panel

	def run(self):
		x, y = (0, 0)
		direction = 0  # 0 is up, 1 is right, 2 is down, 3 is left
		color = {(x, y): self.starting_panel}
		amp = Amplifier(self.program)
		paint = amp.run(self.starting_panel)
		turn = amp.run()
		while not amp.done:
			color[(x, y)] = paint
			direction = (direction + 2 * turn - 1) % 4
			x = x + (direction % 2) * (2 * (direction == 1) - 1)
			y = y + (direction % 2 == 0) * (2 * (direction == 2) - 1)
			paint = amp.run(color.get((x, y), 0))
			turn = amp.run()

		return color


if __name__ == '__main__':
	with open('../inputs/Day11_input.txt', 'r') as f:
		program = list(map(int, f.read().strip().split(',')))

	print(f"The result of first star is {len(EmergencyHullPainting(program[:], 0).run())}")

	colors = EmergencyHullPainting(program[:], 1).run()
	rows = [coord[1] for coord in colors.keys()]
	colons = [coord[0] for coord in colors.keys()]
	r = np.zeros((max(rows) - min(rows) + 1, max(colons) - min(colons) + 1))
	for (x, y), c in colors.items():
		r[y, x] = c

	plt.imshow(np.array(r), cmap=plt.cm.gray)
	plt.show()
