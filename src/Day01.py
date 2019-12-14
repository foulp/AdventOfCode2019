def fuel(mass):
	return int(mass / 3.) - 2

result = 0
with open('../inputs/Day01_input.txt', 'rb') as f:
	for line in f.readlines():
		result += fuel(int(line))

print(f"First star result is {result}")

result = 0
with open('../inputs/Day01_input.txt', 'rb') as f:
	for line in f.readlines():
		module_fuel = fuel(int(line))
		while module_fuel > 0:
			result += module_fuel
			module_fuel = fuel(module_fuel)

print(f"Second star result is {result}")
