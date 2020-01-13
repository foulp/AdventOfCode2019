import re
import math
import networkx as nx


class Reactions:
	def __init__(self, reactions, reactions_inv):
		self.reactions = reactions
		self.reactions_inv = reactions_inv

		network = nx.DiGraph()
		for r in self.reactions:
			for reactif in r.split(', '):
				network.add_edge(reactif.split(' ')[1], self.reactions[r].split(' ')[1])
		self.network = network
		self.dist = nx.single_source_shortest_path_length(self.network, 'ORE')

	def find_agents(self, chemical, n):
		agents = []
		v = next(r for r in self.reactions_inv if chemical in r)
		n_chemical = int(re.search(r'(\d+)', v).group(1))
		for r in self.reactions_inv[v].split(', '):
			m, agent = r.split(' ')
			agents.append((int(m) * math.ceil(n / n_chemical), agent))
		return agents


if __name__ == '__main__':
	with open('../inputs/Day14_input.txt', 'r') as f:
		reactions = f.read().strip().split('\n')
		reactions = dict([r.split(' => ') for r in reactions])

	reactions = {'10 ORE': '10 A', '1 ORE': '1 B', '7 A, 1 B': '1 C', '7 A, 1 C': '1 D', '7 A, 1 D': '1 E', '7 A, 1 E': '1 FUEL'}
	reactions_inv = {reactions[v]: v for v in reactions}

	chemical_reactions = Reactions(reactions, reactions_inv)

	needed = {'FUEL': 1}

	while list(needed.keys()) != ['ORE']:
		temp = {}
		for chemical in needed:
			for n, agent in chemical_reactions.find_agents(chemical, needed[chemical]):
				temp[agent] = temp.get(agent, 0) + n
		needed = dict(temp)

	print(f'The result of first star is {needed["ORE"]}')
