def find_agents(chemical, reactions):

	return []


if __name__ == '__main__':
	with open('../inputs/Day14_input.txt', 'r') as f:
		reactions = f.read().strip().split('\n')
		reactions = dict([r.split(' => ') for r in reactions])

	reactions = {'10 ORE': '10 A', '1 ORE': '1 B', '7 A, 1 B': '1 C', '7 A, 1 C': '1 D', '7 A, 1 D': '1 E', '7 A, 1 E': '1 FUEL'}

	needed = {'FUEL': 1}

	while list(needed.keys()) != ['ORE']:
		temp = {}
		for chemical in needed:
			for n, agent in find_agents(chemical, reactions):
				temp[agent] = temp.get(agent, 0) + n
		needed = dict(temp)

	print(f'The result of first star is {needed["ORE"]}')
