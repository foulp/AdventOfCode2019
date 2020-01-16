import matplotlib.pyplot as plt
import numpy as np
from src.lib.intcode import Amplifier


def plot_game(tiles):
	colors = [0, 1, 2, 1, 3]
	rows = tiles[:-1:3]
	colons = tiles[1::3]
	values = tiles[2::3]
	r = np.zeros((max(colons) - min(colons) + 1, max(rows) - min(rows) + 1))
	for x, y, c in zip(rows, colons, values):
		if not (x == -1 and y == 0):
			r[y, x] = colors[c]
	plt.imshow(r)
	plt.show()


def next_move(board):
	paddle = next((i for i in range(len(board) - 1, 0, -1) if board[i] == 3), 2)
	xp = board[paddle-2]
	ball = next((i for i in range(len(board) - 1, 0, -1) if board[i] == 4), 2)
	xb = board[ball-2]
	ball = next((i for i in range(ball - 1, 0, -1) if board[i] == 3), 0)
	if ball:
		xb_1 = board[ball-2]
	else:
		xb_1 = xb - 1
	xb += (xb - xb_1)

	return np.sign(xb - xp)


if __name__ == '__main__':
	with open('../inputs/Day13_input.txt', 'r') as f:
		program = list(map(int, f.read().strip().split(',')))

	outputs = []
	amp = Amplifier(program[:])
	while not amp.done:
		outputs.append(amp.run())
	print(f"The result of first star is {sum([tile_id == 2 for tile_id in outputs[2::3]])}.")
	program[0] = 2
	amp = Amplifier(program[:])
	pos_tile = []
	outputs = [amp.run(), amp.run(), amp.run()]
	while not amp.done:
		amp.inputs = [next_move(outputs)]
		value = amp.run()
		if len(pos_tile) <= 2:
			pos_tile.append(value)
		if len(pos_tile) == 3:
			if pos_tile[:2] == [-1, 0]:
				print(f"Current score is {pos_tile[2]}")
			else:
				outputs.extend(pos_tile)
			if pos_tile[2] == 4: print(f"Ball is at {pos_tile[:2]}")
			if pos_tile[2] == 3:
				print(f"Paddle is at {pos_tile[:2]}")
				#plot_game(outputs)
			pos_tile = []
