from src.lib.intcode import Amplifier

if __name__ == '__main__':
	with open('../inputs/Day11_input.txt', 'r') as f:
		program = list(map(int, f.read().strip().split(',')))

	x, y = (0, 0)
	direction = 0  # 0 is up, 1 is right, 2 is down, 3 is left
	color = {(x, y): 0}
	amp = Amplifier(program)
	while not amp.done:
		if (x, y) not in color:
			color[(x, y)] = 0
		paint = amp.run(color[(x, y)])
		turn = amp.run(color[(x, y)])
		assert paint in [0, 1]
		assert turn in [0, 1]
		color[(x, y)] = paint
		direction = (direction + 2 * turn - 1) % 4
		x = x + (direction % 2) * (2 * (direction == 1) - 1)
		y = y + (direction % 2 == 0) * (2 * (direction == 2) - 1)

	print(f"The result of first star is {len(color)}")
