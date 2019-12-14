from src.Day07 import Amplifier

if __name__ == '__main__':
	with open("../inputs/Day09_input.txt", "r") as f:
		program = list(map(int, f.read().strip().split(',')))

	program_1 = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
	amp = Amplifier(program_1)
	print(amp.run())

	program_2 = [1102, 34915192, 34915192, 7, 4, 7, 99, 0]
	assert len(str(Amplifier(program_2).run())) == 16

	program_3 = [104, 1125899906842624, 99]
	assert Amplifier(program_3).run() == program_3[1]

	print(f"The result of first star is {Amplifier(program).run(1)}")
