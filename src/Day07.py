from src.lib.intcode import Amplifier
import itertools


def thruster(programme, sequences, first_input=0, feedback=False):
	amps = [Amplifier(programme[:], s, 0) for s in sequences]
	output_value = int(first_input)
	for i in itertools.cycle(range(len(sequences))):
		output_value = amps[i].run(output_value)
		if feedback is False and (i+1) % len(sequences) == 0:
			break
		if feedback and amps[-1].done:
			break
	return amps[-1].value


def find_max_thruster(programme, range_iter=range(5), first_input=0, feedback=False):
	return max((thruster(programme, seq, first_input, feedback), seq) for seq in itertools.permutations(range_iter))


if __name__ == '__main__':
	with open('../inputs/Day07_input.txt', 'r') as f:
		program = f.read().strip()

	program_1 = [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0]
	assert find_max_thruster(program_1) == (43210, (4, 3, 2, 1, 0))

	program_2 = [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0]
	assert find_max_thruster(program_2) == (54321, (0, 1, 2, 3, 4))

	program_3 = [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33, 1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0]
	assert find_max_thruster(program_3) == (65210, (1, 0, 4, 3, 2))

	program = list(map(int, program.split(',')))
	print(f"Result of first star is {find_max_thruster(program)[0]}")

	program_4 = [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5]
	assert thruster(program_4, sequences=(9, 8, 7, 6, 5), feedback=True) == 139629729
	assert find_max_thruster(program_4, range_iter=range(5, 10), feedback=True) == (139629729, (9, 8, 7, 6, 5))

	program_2 = [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54, -5, 54, 1105,
				 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4, 53, 1001, 56, -1, 56, 1005,
				 56, 6, 99, 0, 0, 0, 0, 10]
	assert thruster(program_2, sequences=(9,7, 8, 5, 6), feedback=True) == 18216
	assert find_max_thruster(program_2, range_iter=range(5, 10), feedback=True) == (18216, (9, 7, 8, 5, 6))

	print(f"Result of second star is {find_max_thruster(program, range_iter=range(5,10), feedback=True)[0]}")