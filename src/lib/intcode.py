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

        while self.opcode_plus():
            pass

        return self.value

    def opcode_plus(self):
        instruction = self.program[self.pointer]
        opcode = instruction % 100
        modes = instruction // 100

        # Get first parameter
        if modes % 10 == 1:
            param_1 = self.pointer + 1
        else:
            param_1 = self.program[self.pointer + 1] + self.relative_base * (modes % 10 == 2)

        # Get second and third parameter if needed
        param_2, param_3 = None, None
        if opcode in [1, 2, 5, 6, 7, 8]:
            if modes//10 % 10 == 1:
                param_2 = self.pointer + 2
            else:
                param_2 = self.program[self.pointer + 2] + self.relative_base * (modes // 10 % 10 == 2)
        if opcode in [1, 2, 7, 8]:
            if modes//100 % 10 == 1:
                param_3 = self.pointer + 3
            else:
                param_3 = self.program[self.pointer + 3] + self.relative_base * (modes // 100 % 10 == 2)

        # Increase program length for parameters
        if opcode in [1, 2, 7, 8]:
            self.program += [0] * max(0, max(param_1, param_2, param_3)-len(self.program)+1)
        elif opcode in [5, 6]:
            self.program += [0] * max(0, max(param_1, param_2)-len(self.program)+1)
        elif opcode in [3, 4, 9]:
            self.program += [0] * max(0, param_1-len(self.program)+1)

        # Do action
        if opcode in [1, 2, 3, 5, 6, 7, 8, 9]:
            if opcode == 1:
                self.program[param_3] = self.program[param_1] + self.program[param_2]
                self.pointer += 4
            elif opcode == 2:
                self.program[param_3] = self.program[param_1] * self.program[param_2]
                self.pointer += 4
            elif opcode == 3:
                self.program[param_1] = self.inputs.pop(0) if len(self.inputs) else int(input("Input value?"))
                self.pointer += 2
            elif opcode == 5:
                self.pointer = self.program[param_2] if self.program[param_1] != 0 else self.pointer + 3
            elif opcode == 6:
                self.pointer = self.program[param_2] if self.program[param_1] == 0 else self.pointer + 3
            elif opcode == 7:
                self.program[param_3] = 1 if self.program[param_1] < self.program[param_2] else 0
                self.pointer += 4
            elif opcode == 8:
                self.program[param_3] = 1 if self.program[param_1] == self.program[param_2] else 0
                self.pointer += 4
            elif opcode == 9:
                self.relative_base += self.program[param_1]
                self.pointer += 2

            return 1

        elif opcode == 4:
            self.pointer += 2
            self.value = self.program[param_1]
            return 0

        elif opcode == 99:
            self.done = True
            return 0

        raise ValueError(f"opcode should not be equal to {opcode}")
