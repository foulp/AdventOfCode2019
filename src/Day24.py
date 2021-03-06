import numpy as np


class Eris:
    def __init__(self, array):
        self.grid = array

    def propagate_bugs(self):
        m = np.array(self.grid)
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                k = self.sum_adjacent_tiles(i, j)
                if self.grid[i, j] == '#':
                    m[i, j] = '#' if k == 1 else '.'
                elif self.grid[i, j] == '.':
                    m[i, j] = '#' if k in [1, 2] else '.'

        self.grid = np.array(m)

    def get_biodiversity_rating(self):
        return sum((c == '#') * 2 ** i for i, c in enumerate(self.grid.ravel()))

    def sum_adjacent_tiles(self, i, j):
        k = (self.grid[max(0, i - 1): min(self.grid.shape[0], i + 2), j] == '#').sum()
        k += (self.grid[i, max(0, j - 1): min(self.grid.shape[1], j + 2)] == '#').sum()
        return k if self.grid[i, j] == '.' else k-2


class PlutonianSettlement:
    def __init__(self, array):
        self.grids = {0: array}
        self.shape = array.shape

    def propagate_bugs(self, minutes):
        for n in range(1, minutes+1):
            self.grids[-n] = np.array(['.']*(self.shape[0] * self.shape[1])).reshape(self.shape)
            self.grids[-n][self.shape[0] // 2, self.shape[1] // 2] = '?'
            self.grids[n] = np.array(['.']*(self.shape[0] * self.shape[1])).reshape(self.shape)
            self.grids[n][self.shape[0] // 2, self.shape[1] // 2] = '?'
            m = {i: np.array(self.grids[i]) for i in self.grids}

            for level in self.grids:
                for i in range(self.shape[0]):
                    for j in range(self.shape[1]):
                        if self.grids[level][i, j] == '?':
                            continue
                        k = self.sum_adjacent_tiles(i, j, level, n)
                        if self.grids[level][i, j] == '#':
                            m[level][i, j] = '#' if k == 1 else '.'
                        elif self.grids[level][i, j] == '.':
                            m[level][i, j] = '#' if k in [1, 2] else '.'

            self.grids = {level: np.array(m[level]) for level in m}

    def get_biodiversity_rating(self):
        return sum((g == '#').sum() for g in self.grids.values())

    def sum_adjacent_tiles(self, i, j, level, n):
        k = (self.grids[level][max(0, i - 1): min(self.shape[0], i + 2), j] == '#').sum()
        k += (self.grids[level][i, max(0, j - 1): min(self.shape[1], j + 2)] == '#').sum()

        if i == 0 and level < n:
            k += self.grids[level+1][self.shape[0] // 2 - 1, self.shape[1] // 2] == '#'
        elif i == self.shape[0] - 1 and level < n:
            k += self.grids[level+1][self.shape[0] // 2 + 1, self.shape[1] // 2] == '#'
        elif i == self.shape[0] // 2 - 1 and j == self.shape[1] // 2 and level > -n:
            k += (self.grids[level-1][0, :] == '#').sum()
        elif i == self.shape[0] // 2 + 1 and j == self.shape[1] // 2 and level > -n:
            k += (self.grids[level-1][-1, :] == '#').sum()

        if j == 0 and level < n:
            k += self.grids[level+1][self.shape[0] // 2, self.shape[1] // 2 - 1] == '#'
        elif j == self.shape[0] - 1 and level < n:
            k += self.grids[level+1][self.shape[0] // 2, self.shape[1] // 2 + 1] == '#'
        elif j == self.shape[0] // 2 - 1 and i == self.shape[1] // 2 and level > -n:
            k += (self.grids[level-1][:, 0] == '#').sum()
        elif j == self.shape[0] // 2 + 1 and i == self.shape[1] // 2 and level > -n:
            k += (self.grids[level-1][:, -1] == '#').sum()

        return k if self.grids[level][i, j] == '.' else k - 2


if __name__ == '__main__':
    with open('../inputs/Day24_input.txt', 'r') as f:
        grid = f.read().split('\n')
        grid = np.array([[c for c in row] for row in grid])

    eris = Eris(grid[:, :])
    history = []
    while ''.join(eris.grid.ravel()) not in history:
        history.append(''.join(eris.grid.ravel()))
        eris.propagate_bugs()

    print(f"The result of first star is {eris.get_biodiversity_rating()}")

    n_minutes = 200
    grid[2, 2] = '?'
    pluto = PlutonianSettlement(grid[:, :])
    pluto.propagate_bugs(n_minutes)
    print(f"The result of second star is {pluto.get_biodiversity_rating()}")
