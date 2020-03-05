import networkx as nx
from networkx.algorithms.shortest_paths.generic import shortest_path
import numpy as np
import time

alphabet = ''.join(chr(i) for i in range(ord('A'), ord('Z')+1))


class Maze:
    def __init__(self, grid, n=1):
        self.grid = grid
        self.graph = nx.Graph()
        self.doors = {}
        self.keys = {}

        x, y = np.where(grid == '@')
        self.start = ((x[0], y[0]),)
        if n == 4:
            self.start = ((x[0]+1, y[0]+1), (x[0]+1, y[0]-1), (x[0]-1, y[0]+1), (x[0]-1, y[0]-1))
            for i, j in self.start:
                grid[i, j] = '@'
            grid[(x[0], y[0]+1)] = grid[(x[0], y[0]-1)] = grid[(x[0]+1, y[0])] = grid[(x[0]-1, y[0])] = '#'

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
                        self.graph.add_edge((x, y), (i, j))

    def shortest_path(self):
        shortest = self.grid.shape[0] * self.grid.shape[1] * len(self.keys)
        visited = {(self.start, ''): 0}
        queue = [{'pos': self.start, 'keys': '', 'length': 0}]
        while len(queue):
            current = queue.pop(0)
            if current['length'] >= shortest-2:
                continue
            if visited[(current['pos'], ''.join(sorted(current['keys'])))] < current['length']:
                continue

            for start, pickup, dist in self.accessible_keys(current):
                situation = {'pos': tuple(self.keys[pickup[-1]] if p == start else p for p in current['pos']),
                             'keys': current['keys']+pickup,
                             'length': current['length']+dist}

                if visited.get((situation['pos'], ''.join(sorted(situation['keys']))), 10**6) <= situation['length']:
                    continue
                visited[(situation['pos'], ''.join(sorted(situation['keys'])))] = situation['length']

                if len(situation['keys']) == len(self.keys):
                    print(situation['keys'], situation['length'])
                    shortest = min(shortest, situation['length'])
                    continue

                queue.append(situation)

        return shortest

    def accessible_keys(self, situation):
        candidates = self.keys.keys() - situation['keys']
        for key in candidates:
            for pos in situation['pos']:
                if not nx.has_path(self.graph, pos, self.keys[key]):
                    continue
                path = shortest_path(self.graph, pos, self.keys[key])
                pickup = ''
                opened = True
                for case in path[1:-1]:
                    if self.grid[case] in alphabet and self.grid[case].lower() not in situation['keys']:
                        opened = False
                        break
                    if self.grid[case] in candidates:
                        pickup += self.grid[case]

                if opened:
                    yield pos, pickup+key, len(path) - 1
                break


if __name__ == '__main__':
    with open('../inputs/Day18_input.txt', 'r') as f:
        grid = f.read().split('\n')
        grid = np.array([[c for c in row] for row in grid])

    maze = Maze(grid)
    t = time.time()
    print(f"The result of first star is {maze.shortest_path()}")
    print(time.time()-t)

    t = time.time()
    maze = Maze(grid, n=4)
    print(f"The result of second star is {maze.shortest_path()}")
    print(time.time() - t)
