import networkx as nx
import numpy as np

alphabet = ''.join(chr(i) for i in range(ord('A'), ord('Z')+1))


class Maze:
    def __init__(self, grid, n=1):
        self.grid = grid
        self.graph = nx.Graph()
        self.portals = {}

        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if grid[i, j] in '# ':
                    continue

                elif grid[i, j] in alphabet:
                    if i+1 < grid.shape[0] and i > 0 and grid[i+1, j] in alphabet and grid[i-1, j] == '.':
                        code_portal = grid[i, j] + grid[i+1, j]
                        layer = 2 * (i < self.grid.shape[0] / 2) - 1
                        self.portals[code_portal] = self.portals.get(code_portal, []) + [((i-1, j), layer)]

                    elif i+2 < grid.shape[0] and grid[i+1, j] in alphabet and grid[i+2, j] == '.':
                        code_portal = grid[i, j] + grid[i+1, j]
                        layer = 2 * (i > self.grid.shape[0] / 2) - 1
                        self.portals[code_portal] = self.portals.get(code_portal, []) + [((i+2, j), layer)]

                    elif j+2 < grid.shape[1] and grid[i, j+1] in alphabet and grid[i, j+2] == '.':
                        code_portal = grid[i, j] + grid[i, j+1]
                        layer = 2 * (j > self.grid.shape[1] / 2) - 1
                        self.portals[code_portal] = self.portals.get(code_portal, []) + [((i, j+2), layer)]

                    elif j+1 < grid.shape[1] and j > 0 and grid[i, j+1] in alphabet and grid[i, j-1] == '.':
                        code_portal = grid[i, j] + grid[i, j+1]
                        layer = 2 * (j < self.grid.shape[1] / 2) - 1
                        self.portals[code_portal] = self.portals.get(code_portal, []) + [((i, j-1), layer)]

                elif grid[i, j] == '.':
                    for depth in range(n):
                        self.graph.add_node((i, j, depth))
                    for x, y in [(i-1, j), (i, j-1)]:
                        for depth in range(n):
                            if (x, y, depth) in self.graph:
                                self.graph.add_edge((x, y, depth), (i, j, depth))

        for code, elements in self.portals.items():
            if code == 'AA':
                self.start = elements[0][0] + (0,)
            elif code == 'ZZ':
                self.end = elements[0][0] + (0,)
            else:
                if n > 1:
                    for depth in range(n):
                        self.graph.add_edge(elements[0][0] + (depth,), elements[1][0] + (depth + elements[0][1],))
                        self.graph.add_edge(elements[0][0] + (depth + elements[1][1],), elements[1][0] + (depth,))
                else:
                    self.graph.add_edge(elements[0][0] + (0,), elements[1][0] + (0,))


if __name__ == '__main__':
    with open('../inputs/Day20_input.txt', 'r') as f:
        grid = f.read().split('\n')
        grid[-1] += ' ' * (len(grid[0]) - len(grid[-1]))
        grid = np.array([[c for c in row] for row in grid])

    maze = Maze(grid, n=1)
    print(f"The result of first star is {len(nx.shortest_path(maze.graph, maze.start, maze.end)) - 1}")

    n = 2
    while True:
        maze = Maze(grid, n=n)
        if nx.has_path(maze.graph, maze.start, maze.end):
            print(f"The result of second star is {len(nx.shortest_path(maze.graph, maze.start, maze.end)) - 1}")
            print(f"Needed depth = {n}")
            break
        n += 1
