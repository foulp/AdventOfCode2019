from src.lib.intcode import opcode_plus

if __name__ == '__main__':
	with open("../inputs/Day05_input.txt", "r") as f:
		intcode_txt = f.read()

	program = list(map(int, intcode_txt.split(',')))
	dico = {"pointeur": 0, "output": 1, "program": program, "inputs": [1]}
	r = []
	c = 0
	while dico["output"] > 0:
		dico = opcode_plus(dico["program"], dico["pointeur"], dico["inputs"])
		c += 1
		if dico["output"] != 1:
			r.append((c, dico))

	assert r[-1][1]["output"] == 0
	assert r[-1][0] == r[-2][0] + 1
	assert all(v[1]["value"] == 0 for v in r[:-2])

	print(f'Result of first star is {r[-2][1]["value"]}')

	program = list(map(int, intcode_txt.split(',')))
	dico = {"pointeur": 0, "output": 1, "program": program, "inputs": [5]}
	r = []
	c = 0
	while dico["output"] > 0:
		dico = opcode_plus(dico["program"], dico["pointeur"], dico["inputs"])
		c += 1
		if dico["output"] != 1:
			r.append((c, dico))

	assert r[-1][1]["output"] == 0
	assert len(r) == 2
	print(f'Result of second star is {r[-2][1]["value"]}')
