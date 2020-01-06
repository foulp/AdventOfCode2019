class Amplifier:
    def __init__(self, program, setting=None, pointer=0, relative_base=0):
        self.program = program
        if setting is not None:
            self.inputs = [setting]
        else:
            self.inputs = []
        self.pointer = pointer
        self.relative_base = relative_base
        self.done = False
        self.value = None

    def run(self, value=None):
        if value is not None:
            self.inputs.append(value)
        dico = {"output": 1, "program": self.program, "pointer": self.pointer, "inputs": self.inputs,
                "relative_base": 0}
        while dico["output"] == 1:
            dico = opcode_plus(dico["program"], dico["pointer"], dico["inputs"], dico["relative_base"])

        if dico["output"] == 99:
            self.done = True
            return self.value

        self.value = dico["value"]
        self.program = dico["program"]
        self.pointer = dico["pointer"]
        self.relative_base = dico["relative_base"]
        self.inputs = dico["inputs"]
        return self.value


def opcode_plus(program, pointer=0, inputs=[], relative_base=0):
    instruction = program[pointer]
    opcode = instruction % 100
    modes = instruction // 100

    # Get first parameter
    if modes % 10 == 1:
        param_1 = pointer + 1
    else:
        param_1 = program[pointer + 1] + relative_base * (modes % 10 == 2)

    # Get second and third parameter if needed
    param_2, param_3 = None, None
    if opcode in [1, 2, 5, 6, 7, 8]:
        if modes//10 % 10 == 1:
            param_2 = pointer + 2
        else:
            param_2 = program[pointer + 2] + relative_base * (modes // 10 % 10 == 2)
    if opcode in [1, 2, 7, 8]:
        if modes//100 % 10 == 1:
            param_3 = pointer + 3
        else:
            param_3 = program[pointer + 3] + relative_base * (modes // 100 % 10 == 2)

    # Increase program length for parameters
    if opcode in [1, 2, 7, 8]:
        program += [0] * max(0, max(param_1, param_2, param_3)-len(program)+1)
    elif opcode in [5, 6]:
        program += [0] * max(0, max(param_1, param_2)-len(program)+1)
    elif opcode in [3, 4, 9]:
        program += [0] * max(0, param_1-len(program)+1)

    # Do action
    if opcode in [1, 2, 3, 5, 6, 7, 8, 9]:
        if opcode == 1:
            program[param_3] = program[param_1] + program[param_2]
            pointer += 4
        elif opcode == 2:
            program[param_3] = program[param_1] * program[param_2]
            pointer += 4
        elif opcode == 3:
            program[param_1] = inputs.pop(0) if len(inputs) else int(input("Input value?"))
            pointer += 2
        elif opcode == 5:
            pointer = program[param_2] if program[param_1] != 0 else pointer + 3
        elif opcode == 6:
            pointer = program[param_2] if program[param_1] == 0 else pointer + 3
        elif opcode == 7:
            program[param_3] = 1 if program[param_1] < program[param_2] else 0
            pointer += 4
        elif opcode == 8:
            program[param_3] = 1 if program[param_1] == program[param_2] else 0
            pointer += 4
        elif opcode == 9:
            relative_base += program[param_1]
            pointer += 2

        return {"output": 1, "program": program, "pointer": pointer, "inputs": inputs, "relative_base": relative_base}

    elif opcode == 4:
        pointer += 2
        return {"output": 2, "program": program, "pointer": pointer, "inputs": inputs, "relative_base": relative_base,
                "value": program[param_1]}

    elif opcode == 99:
        return {"output": 99}

    raise ValueError(f"opcode should not be equal to {opcode}")
