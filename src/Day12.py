import itertools
import numpy as np
import re

REGEX = r'-?\d+'


class Moon:
	def __init__(self, pos):
		x, y, z = pos
		self.x = int(x)
		self.y = int(y)
		self.z = int(z)
		self.vx = 0
		self.vy = 0
		self.vz = 0

	def update_position(self):
		self.x += self.vx
		self.y += self.vy
		self.z += self.vz

	def update_velocity(self, gx, gy, gz):
		self.vx += gx
		self.vy += gy
		self.vz += gz

	def get_kinetic_energy(self):
		return abs(self.vx) + abs(self.vy) + abs(self.vz)

	def get_potential_energy(self):
		return abs(self.x) + abs(self.y) + abs(self.z)

	def get_total_energy(self):
		return self.get_potential_energy() * self.get_kinetic_energy()


class System:
	def __init__(self, moons):
		self.m1 = Moon(re.findall(REGEX, moons[0]))
		self.m2 = Moon(re.findall(REGEX, moons[1]))
		self.m3 = Moon(re.findall(REGEX, moons[2]))
		self.m4 = Moon(re.findall(REGEX, moons[3]))
		self.starting_state = [Moon(re.findall(REGEX, moons[i])) for i in range(4)]

	def get_moons(self):
		return [self.m1, self.m2, self.m3, self.m4]

	def update(self):
		for m1, m2 in itertools.combinations(self.get_moons(), 2):
			gx = -1 if m1.x > m2.x else 1 if m1.x < m2.x else 0
			gy = -1 if m1.y > m2.y else 1 if m1.y < m2.y else 0
			gz = -1 if m1.z > m2.z else 1 if m1.z < m2.z else 0

			m1.update_velocity(gx, gy, gz)
			m2.update_velocity(-gx, -gy, -gz)

		for m in self.get_moons():
			m.update_position()

	def equal_previous_state_dim(self, dim):
		for i in range(1, 5):
			state = self.starting_state[i-1]
			if eval(f'state.{dim}') != eval(f'self.m{i}.{dim}') or eval(f'state.v{dim}') != eval(f'self.m{i}.v{dim}'):
				return False
		return True

	def get_total_energy(self):
		return sum(m.get_total_energy() for m in self.get_moons())


def final_energy(moons, time_steps):
	system = System(moons)
	for _ in range(time_steps):
		system.update()

	return system.get_total_energy()


def identical_state(moons):
	system = System(moons)
	time_steps = 0
	dim = {'x': 0, 'y': 0, 'z': 0}
	while any(dim[d] == 0 for d in dim):
		system.update()
		time_steps += 1
		for v in [k for k in dim.keys() if dim[k] == 0]:
			if system.equal_previous_state_dim(v):
				dim[v] = time_steps
	return np.lcm.reduce(list(dim.values()), dtype=np.int64)


if __name__ == '__main__':
	with open('../inputs/Day12_input.txt', 'r') as f:
		moons = f.read().strip().split('\n')

	moons_1 = ["<x=-1, y=0, z=2>", "<x=2, y=-10, z=-7>", "<x=4, y=-8, z=8>", "<x=3, y=5, z=-1>"]
	assert final_energy(moons_1, 10) == 179

	moons_2 = ['<x=-8, y=-10, z=0>', '<x=5, y=5, z=10>', '<x=2, y=-7, z=3>', '<x=9, y=-8, z=-3>']
	assert final_energy(moons_2, 100) == 1940

	print(f"The result of first star is {final_energy(moons, 1000)}")

	assert identical_state(moons_1) == 2772
	print("Assert 1 OK")
	assert identical_state(moons_2) == 4686774924
	print("Assert 2 OK")
	print(f"The result of second star is {identical_state(moons)}")
