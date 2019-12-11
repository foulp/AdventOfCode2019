def opcode_plus(program, pointeur=0, inputs=[], relative_base=0):
	instruction = program[pointeur]
	opcode = instruction % 100
	modes = instruction // 100

	if opcode in [1, 2, 4, 5, 6, 7, 8, 9]:
		if modes%10 == 1:
			param_1 = program[pointeur+1]
		else:
			param_1 = program[program[pointeur+1]  + relative_base*(modes%10==2)]
	if opcode in [1, 2, 5, 6, 7, 8]:
		if modes//10 == 1:
			param_2 = program[pointeur+2]
		else:
			param_2 = program[program[pointeur+2] + relative_base*(modes//10==2)]


	if opcode in [1, 2, 3, 5, 6, 7, 8, 9]:
		if opcode in [1, 2, 7, 8]:
			program += [0] * max(0, program[pointeur+3]-len(program)+1)
		if opcode == 3:
			program += [0] * max(0, program[pointeur+1]-len(program)+1)

		if opcode == 1: 
			program[program[pointeur+3]] = param_1 + param_2
			pointeur += 4
		elif opcode == 2: 
			program[program[pointeur+3]] = param_1 * param_2
			pointeur += 4
		elif opcode == 3:
			program[program[pointeur+1]] = inputs.pop(0) if len(inputs) else int(input("Input value?"))
			pointeur += 2
		elif opcode == 5: 
			pointeur = param_2 if param_1!=0 else pointeur+3
		elif opcode == 6: 
			pointeur = param_2 if param_1==0 else pointeur+3
		elif opcode == 7:
			program[program[pointeur+3]] = 1 if param_1 < param_2 else 0
			pointeur += 4
		elif opcode == 8: 
			program[program[pointeur+3]] = 1 if param_1 == param_2 else 0
			pointeur += 4
		elif opcode == 9:
			relative_base += param_1
			pointeur += 2

		return {"output": 1, "program": program, "pointeur": pointeur, "inputs": inputs, "relative_base": relative_base}


	elif opcode == 4:
		pointeur += 2
		return {"output": 2, "program": program, "pointeur": pointeur, "inputs": inputs, "relative_base": relative_base, "value": param_1}

	elif opcode == 99:
		return {"output": 0}

	raise ValueError(f"opcode shouldn't be equal to {opcode}")

if __name__ == '__main__':
	with open("Day05_input.txt", "r") as f:
		intcode_txt = f.read()

	program = list(map(int, intcode_txt.split(',')))
	dico = {"pointeur": 0, "output": 1, "program": program}
	r = []
	c = 0
	while dico["output"] > 0:
		dico = opcode_plus(dico["program"], dico["pointeur"])
		c += 1
		if dico["output"] != 1:
			r.append((c, dico))

	assert r[-1][1]["output"] == 0
	assert r[-1][0] == r[-2][0] + 1
	assert all(v[1]["value"] == 0 for v in r[:-2])

	print(f'Result of first star is {r[-2][1]["value"]}')


	program = list(map(int, intcode_txt.split(',')))
	dico = {"pointeur": 0, "output": 1, "program": program}
	r = []
	c = 0
	while dico["output"] > 0:
		dico = opcode_plus(dico["program"], dico["pointeur"])
		c += 1
		if dico["output"] != 1:
			r.append((c, dico))

	assert r[-1][1]["output"] == 0
	assert len(r) == 2
	print(f'Result of second star is {r[-2][1]["value"]}')