import matplotlib.pyplot as plt
import numpy as np
from src.lib.intcode import Amplifier

if __name__ == '__main__':
	with open('../inputs/Day13_input.txt', 'r') as f:
		program = list(map(int, f.read().strip().split(',')))

	outputs = []
	amp = Amplifier(program[:])
	while not amp.done:
		outputs.append(amp.run())
	print(f"The result of first star is {sum([tile_id == 2 for tile_id in outputs[2::3]])}.")

	colors = [0, 1, 2, 1, 3]
	rows = outputs[:-1:3]
	colons = outputs[1::3]
	values = outputs[2::3]
	r = np.zeros((max(colons) - min(colons) + 1, max(rows) - min(rows) + 1))
	for x, y, c in zip(rows, colons, values):
		r[y, x] = colors[c]
	plt.imshow(r)
	plt.show()

	program[0] = 2
	outputs = []
	amp = Amplifier(program[:])
	while not amp.done:
		outputs.append(amp.run(np.random.randint(0, 3)))
		if len(outputs) > 2 and outputs[-1] == 0 and outputs[-2] == -1:
			print(outputs[0], len(outputs))

	k = next(i for i in range(len(outputs) - 1, 0, -1) if outputs[i] == 0 and outputs[i-1] == -1)
	print(f"The result of second star is {outputs[k+1]}")
