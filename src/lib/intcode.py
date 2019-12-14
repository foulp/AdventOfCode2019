class Amplifier:
    def __init__(self, program, setting=None, pointeur=0, relative_base=0):
        self.program = program
        if setting is not None:
            self.inputs = [setting]
        else:
            self.inputs = []
        self.pointeur = pointeur
        self.relative_base = relative_base
        self.done = False
        self.value = None

    def run(self, value=None):
        if value is not None:
            self.inputs.append(value)
        dico = {"output": 1, "program": self.program, "pointeur": self.pointeur, "inputs": self.inputs,
                "relative_base": 0}
        while dico["output"] == 1:
            dico = opcode_plus(dico["program"], dico["pointeur"], dico["inputs"], dico["relative_base"])

        if dico["output"] == 99:
            self.done = True
            return self.value

        self.value = dico["value"]
        self.program = dico["program"]
        self.pointeur = dico["pointeur"]
        self.relative_base = dico["relative_base"]
        self.inputs = dico["inputs"]
        return self.value


def opcode_plus(program, pointeur=0, inputs=[], relative_base=0):
    instruction = program[pointeur]
    opcode = instruction % 100
    modes = instruction // 100

    param_1, param_2 = None, None
    if opcode in [1, 2, 4, 5, 6, 7, 8, 9]:
        if modes % 10 == 1:
            param_1 = program[pointeur+1]
        else:
            param_1 = program[program[pointeur+1] + relative_base*(modes % 10 == 2)]
    if opcode in [1, 2, 5, 6, 7, 8]:
        if modes//10 == 1:
            param_2 = program[pointeur+2]
        else:
            param_2 = program[program[pointeur+2] + relative_base*(modes//10 == 2)]

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
            pointeur = param_2 if param_1 != 0 else pointeur+3
        elif opcode == 6:
            pointeur = param_2 if param_1 == 0 else pointeur+3
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
        return {"output": 2, "program": program, "pointeur": pointeur, "inputs": inputs, "relative_base": relative_base,
                "value": param_1}

    elif opcode == 99:
        return {"output": 99}

    raise ValueError(f"opcode shouldn't be equal to {opcode}")
