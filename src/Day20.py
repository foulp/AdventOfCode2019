import networkx as nx
import numpy as np

alphabet = ''.join(chr(i) for i in range(ord('A'), ord('Z')+1))


class Maze:
    def __init__(self, grid):
        self.grid = grid
        self.graph = nx.Graph()
        self.portals = {}

        x, y = np.where(grid == '@')
        self.start = (x[0], y[0])

        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if grid[i, j] in '# ':
                    continue

                elif grid[i, j] in alphabet:
                    if grid[i-1, j] in alphabet and grid[i-2, j] == '.':
                        self.graph.add_node((i-1, j))
                        self.portals[(i-1, j)] = self.portals.get((i-1, j), []) + [grid[i-1, j] + grid[i, j]]

                    elif grid[i, j-1] in alphabet and grid[i, j-2] == '.':
                        self.graph.add_node((i, j-1))
                        self.portals[(i, j-1)] = self.portals.get((i, j-1), []) + [grid[i, j-1] + grid[i, j]]

                    elif grid[i+1, j] in alphabet and grid[i+2, j] == '.':
                        self.graph.add_node((i+1, j))
                        self.portals[(i+1, j)] = self.portals.get((i+1, j), []) + [grid[i, j] + grid[i+1, j]]

                    elif grid[i, j+1] in alphabet and grid[i, j+2] == '.':
                        self.graph.add_node((i, j+1))
                        self.portals[(i, j+1)] = self.portals.get((i, j+1), []) + [grid[i, j] + grid[i, j+1]]

                elif grid[i, j] == '.':
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


if __name__ == '__main__':
    with open('../inputs/Day18_input.txt', 'r') as f:
        grid = f.read().split('\n')
        grid = np.array([[c for c in row] for row in grid])

    maze = Maze(grid)
    print(f"The result of first star is {nx.shortest_path(maze.graph, maze.start, maze.end)}")
    print(f"The result of second star is {0}")
