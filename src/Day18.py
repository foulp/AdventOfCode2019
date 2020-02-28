import networkx as nx
import numpy as np

alphabet = ''.join(chr(i) for i in range(ord('A'), ord('Z')+1))


class Maze:
    def __init__(self, grid):
        self.grid = grid
        self.graph = nx.Graph()
        self.doors = {}
        self.keys = {}
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if grid[i, j] == '#':
                    continue
                if self.grid[i, j] in alphabet.lower()+'.':
                    if self.grid[i, j] == '.':
                        self.graph.add_node((i, j))
                    else:
                        self.graph.add_node((i, j), name=self.grid[i, j])
                        self.keys[self.grid[i, j]] = (i, j)

                    if (i-1, j) in self.graph:
                        self.graph.add_edge((i-1, j), (i, j))
                    if (i, j-1) in self.graph:
                        self.graph.add_edge((i, j-1), (i, j))
                else:
                    self.graph.add_node((i, j), name=self.grid[i, j])
                    self.doors[self.grid[i, j]] = (i, j)

        x, y = np.where(grid == '@')
        self.x = x[0]
        self.y = y[0]
        self.pickup = []
        self.compteur = 0
        self.high_boundary = grid.shape[0] * grid.shape[1] * len(self.doors)

    def shortest_path(self):
        if len(self.pickup) == len(self.keys[0]):
            self.high_boundary = min(self.high_boundary, self.compteur)
            return True
        if self.compteur >= self.high_boundary:
            return False

        prev_x, prev_y = self.x, self.y
        for key, dist in self.accessible_keys():
            self.x, self.y = self.keys[key]
            self.compteur += dist
            if self.shortest_path():
                return True
            self.compteur -= dist
            self.x, self.y = prev_x, prev_y

        return False

    def accessible_keys(self):

        return []


if __name__ == '__main__':
    with open('../inputs/Day18_input.txt', 'r') as f:
        grid = f.read().split('\n')
        grid = np.array([[c for c in row] for row in grid])

    maze = Maze(grid)

    print(f"The result of first star is {0}")

    print(f"The result of second star is {0}")
