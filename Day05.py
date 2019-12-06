with open("Day05_input.txt", "r") as f:
	intcode_txt = f.read()

def opcode(program, pointeur):
	instruction = program[pointeur]
	a = instruction % 100
	if a in [1, 2]:
		modes = str(instruction // 100)[::-1]
		param_1 = program[program[pointeur+1]] if modes[0]=='0' else program[pointeur+1]
		param_2 = program[program[pointeur+2]] if (len(modes)==1 or modes[1]=='0') else program[pointeur+2]
		if a == 1: program[program[pointeur+3]] = param_1 + param_2
		elif a == 2: program[program[pointeur+3]] = param_1 * param_2
		pointeur += 4
		return {"output": 1, "program": program, "pointeur": pointeur}

	elif a == 3:
		program[program[pointeur+1]] = int(input("Input value?"))
		pointeur += 2
		return {"output": 1, "program": program, "pointeur": pointeur}

	elif a == 4:
		b = instruction // 100
		b = program[pointeur+1] if b==1 else program[program[pointeur+1]]
		pointeur += 2
		return {"output": 2, "program": program, "pointeur": pointeur, "value": b}

	elif a == 99:
		return {"output": 0, "value": 99}

	raise ValueError(f"a shouldn't be equal to {a}")


program = list(map(int, intcode_txt.split(',')))
dico = {"pointeur": 0, "output": 1, "program": program}
r = []
c = 0
while dico["output"] > 0:
	dico = opcode(dico["program"], dico["pointeur"])
	c += 1
	if dico["output"] != 1:
		r.append((c, dico["output"], dico["value"]))

assert r[-1][2] == 99
assert r[-1][0] == r[-2][0] + 1
assert all(v[2] == 0 for v in r[:-2])

print(f"Result of first star is {r[-2][2]}")

def opcode_plus(program, pointeur):
	instruction = program[pointeur]
	a = instruction % 100
	if a in [1, 2, 5, 6, 7, 8]:
		modes = str(instruction // 100)[::-1]
		param_1 = program[program[pointeur+1]] if modes[0]=='0' else program[pointeur+1]
		param_2 = program[program[pointeur+2]] if (len(modes)==1 or modes[1]=='0') else program[pointeur+2]
		if a == 1: 
			program[program[pointeur+3]] = param_1 + param_2
			pointeur += 4
		if a == 2: 
			program[program[pointeur+3]] = param_1 * param_2
			pointeur += 4
		if a == 5: 
			pointeur = param_2 if param_1!=0 else pointeur+3
		if a == 6: 
			pointeur = param_2 if param_1==0 else pointeur+3
		if a == 7:
			program[program[pointeur+3]] = 1 if param_1 < param_2 else 0
			pointeur += 4
		if a == 8: 
			program[program[pointeur+3]] = 1 if param_1 == param_2 else 0
			pointeur += 4

		return {"output": 1, "program": program, "pointeur": pointeur}

	elif a == 3:
		program[program[pointeur+1]] = int(input("Input value?"))
		pointeur += 2
		return {"output": 1, "program": program, "pointeur": pointeur}

	elif a == 4:
		b = instruction // 100
		b = program[pointeur+1] if b==1 else program[program[pointeur+1]]
		pointeur += 2
		return {"output": 2, "program": program, "pointeur": pointeur, "value": b}

	elif a == 99:
		return {"output": 0, "value": 99}

	raise ValueError(f"a shouldn't be equal to {a}")


program = list(map(int, intcode_txt.split(',')))
dico = {"pointeur": 0, "output": 1, "program": program}
r = []
c = 0
while dico["output"] > 0:
	dico = opcode_plus(dico["program"], dico["pointeur"])
	c += 1
	if dico["output"] != 1:
		r.append((c, dico["output"], dico["value"]))

assert r[-1][2] == 99
assert len(r) == 2
print(f"Result of second star is {r[-2][2]}")