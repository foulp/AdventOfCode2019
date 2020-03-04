import networkx as nx
from networkx.algorithms.shortest_paths.generic import shortest_path
import numpy as np

alphabet = ''.join(chr(i) for i in range(ord('A'), ord('Z')+1))


class Maze:
    def __init__(self, grid):
        self.grid = grid
        self.graph = nx.DiGraph()
        self.doors = {}
        self.keys = {}
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if grid[i, j] == '#':
                    continue
                self.graph.add_node((i, j))
                if self.grid[i, j] in alphabet.lower():
                    self.keys[self.grid[i, j]] = (i, j)
                elif self.grid[i, j] in alphabet:
                    self.doors[self.grid[i, j]] = (i, j)

                for x, y in [(i-1, j), (i, j-1)]:
                    if (x, y) in self.graph:
                        if self.grid[x, y] not in alphabet or self.grid[i, j] in alphabet:
                            self.graph.add_edge((x, y), (i, j))

                        if self.grid[i, j] not in alphabet or self.grid[x, y] in alphabet:
                            self.graph.add_edge((i, j), (x, y))

        x, y = np.where(grid == '@')
        self.x = x[0]
        self.y = y[0]

    def shortest_path(self):
        shortest = self.grid.shape[0] * self.grid.shape[1] * len(self.keys)
        visited = {}
        queue = [{'pos': (self.x, self.y), 'keys': '', 'length': 0}]
        while len(queue):
            current = queue.pop(0)
            for key, dist in self.accessible_keys(current):
                situation = {'pos': self.keys[key],
                             'keys': current['keys']+key,
                             'length': current['length'] + dist}
                if visited.get((situation['pos'], ''.join(sorted(situation['keys']))), -1) > situation['length']:
                    continue

                visited[(situation['pos'], ''.join(sorted(situation['keys'])))] = situation['length']
                queue.append(situation)

                if len(situation['keys']) == len(self.keys):
                    print(situation['keys'], situation['length'])
                    shortest = min(shortest, situation['length'])
        return shortest

    def accessible_keys(self, situation):
        for key in situation['keys']:
            if key.upper() in self.doors:
                for n in self.graph.predecessors(self.doors[key.upper()]):
                    self.graph.add_edge(self.doors[key.upper()], n)

        for key in [k for k in self.keys if k not in situation['keys']]:
            if nx.has_path(self.graph, situation['pos'], self.keys[key]):
                yield key, len(shortest_path(self.graph, situation['pos'], self.keys[key])) - 1

        for key in situation['keys']:
            if key.upper() in self.doors:
                for n in self.graph.predecessors(self.doors[key.upper()]):
                    if self.grid[n] not in alphabet:
                        self.graph.add_edge(self.doors[key.upper()], n)


if __name__ == '__main__':
    with open('../inputs/Day18_input.txt', 'r') as f:
        grid = f.read().split('\n')
        grid = np.array([[c for c in row] for row in grid])

    maze = Maze(grid)

    print(f"The result of first star is {maze.shortest_path()}")

    print(f"The result of second star is {0}")
