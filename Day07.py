from Day05 import opcode_plus
import itertools

def thruster(program, sequences, first_input=0, feedback=False, log=False):
	amps = [Amplifier(program[:], s, 0) for s in sequences]
	output_value = int(first_input)
	for i in itertools.cycle(range(len(sequences))):
		output_value = amps[i].run(output_value, log)
		if feedback==False and (i+1) % len(sequences) == 0:
			break
		if feedback and amps[-1].done:
			break
	return amps[-1].value


def find_max_thruster(program, range_iter=range(5), first_input=0, feedback=False, log=False):
	return max((thruster(program, seq, first_input, feedback, log), seq) for seq in itertools.permutations(range_iter))

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

	def run(self, value=None, log=False):
		if value is not None:
			self.inputs.append(value)
		dico = {"output": 1, "program": self.program, "pointeur": self.pointeur, "inputs": self.inputs, "relative_base": 0}
		while dico["output"] == 1:
			dico = opcode_plus(dico["program"], dico["pointeur"], dico["inputs"], dico["relative_base"])
		
		if dico["output"] == 0:
			self.done = True
			return self.value

		self.value = dico["value"]
		self.program = dico["program"]
		self.pointeur = dico["pointeur"]
		self.relative_base = dico["relative_base"]
		self.inputs = dico["inputs"]
		return self.value


if __name__ == '__main__':
	with open('Day07_input.txt', 'r') as f:
		program = f.read().strip()

	assert find_max_thruster([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]) == (43210, (4,3,2,1,0))
	assert find_max_thruster([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0]) == (54321, (0,1,2,3,4))
	assert find_max_thruster([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0]) == (65210, (1,0,4,3,2))

	program = list(map(int, program.split(',')))
	print(f"Result of first star is {find_max_thruster(program)[0]}")

	program_1 = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
	assert thruster(program_1, sequences=(9,8,7,6,5), feedback=True) == 139629729
	assert find_max_thruster(program_1, range_iter=range(5,10), feedback=True) == (139629729, (9,8,7,6,5))


	program_2 = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]
	assert thruster(program_2, sequences=(9,7,8,5,6), feedback=True) == 18216
	assert find_max_thruster(program_2, range_iter=range(5,10), feedback=True) == (18216, (9,7,8,5,6))

	print(f"Result of second star is {find_max_thruster(program, range_iter=range(5,10), feedback=True)[0]}")