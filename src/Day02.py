with open("../inputs/Day02_input.txt", "r") as f:
	intcode_txt = f.read()

intcode = list(map(int, intcode_txt.split(',')))
intcode[1] = 12
intcode[2] = 2


def opcode(a, b, c):
	if a == 1:
		return b + c
	elif a == 2:
		return b * c
	return False


def full_turn(a, b, intcode_txt):
	intcode = list(map(int, intcode_txt.split(',')))
	intcode[1] = a
	intcode[2] = b

	for i in range(0, len(intcode), 4):
		opc = opcode(intcode[i], intcode[intcode[i+1]], intcode[intcode[i+2]])
		if opc is False:
			break
		intcode[intcode[i+3]] = opc

	return intcode[0]


def find_full_turn(v):
	for a in range(100):
		for b in range(100):
			if full_turn(a, b, intcode_txt) == v:
				print(f"Result of second star is {100 * a + b} : ({a}, {b})")
				return True


if __name__ == '__main__':
	for i in range(0, len(intcode), 4):
		opc = opcode(intcode[i], intcode[intcode[i+1]], intcode[intcode[i+2]])
		if opc is False:
			break
		intcode[intcode[i+3]] = opc

	print(f"Result of first star is {intcode[0]}")

	find_full_turn(19690720)
