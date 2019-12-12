import numpy as np

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

def isBetween(a, b, c, epsilon):
    crossproduct = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)

    # compare versus epsilon for floating point values, or != 0 if using integers
    if abs(crossproduct) > epsilon:
        return False

    dotproduct = (c.x - a.x) * (b.x - a.x) + (c.y - a.y)*(b.y - a.y)
    if dotproduct < 0:
        return False

    squaredlengthba = (b.x - a.x)*(b.x - a.x) + (b.y - a.y)*(b.y - a.y)
    if dotproduct > squaredlengthba:
        return False

    return True

def asteros_seen(rows, cols, i, j, epsilon):
	a = Point(rows[i], cols[i])
	b = Point(rows[j], cols[j])

	for k in range(i+1, j):
		c = Point(rows[k], cols[k])
		if isBetween(a, b, c, epsilon):
			return False
	return True

def max_astero_seen(grid, epsilon=0):
	rows, cols = np.where(grid == '#')
	sights = np.zeros((rows.shape[0], rows.shape[0]))
	for i in range(rows.shape[0]):
		for j in range(i+1, cols.shape[0]):
			if asteros_seen(rows, cols, i, j, epsilon):
				sights[i, j] = 1
				sights[j, i] = 1
	return max((v, cols[i], rows[i]) for i, v in enumerate(sights.sum(axis=1)))

if __name__ == '__main__':
	with open('Day10_input.txt', 'r') as f:
		grid = np.array([[c for c in line] for line in f.read().strip().split('\n')])

	grid_1 = np.array(list('.#..#.....#####....#...##')).reshape(5, 5)
	
	grid_2 = np.array(list('......#.#.#..#.#......#######..#.#.###...#..#.......#....#.##..#....#..##.#..#####...#..#..#....####'))
	grid_2 = grid_2.reshape(10, 10)
	
	grid_3 = np.array(list('#.#...#.#..###....#..#....#...##.#.#.#.#....#.#.#..##..###.#..#...##....##....##......#....####.###.'))
	grid_3 = grid_3.reshape(10, 10)

	grid_4 = np.array(list('.#..#..#######.###.#....###.#...###.##.###.##.#.#.....###..#..#.#..#.##..#.#.###.##...##.#.....#.#..'))
	grid_4 = grid_4.reshape(10, 10)

	assert max_astero_seen(grid_1) == (8, 3, 4)
	print("assert 1 OK")
	assert max_astero_seen(grid_2) == (33, 5, 8) 
	print("assert 2 OK")
	assert max_astero_seen(grid_3) == (35, 1, 2)
	print("assert 3 OK")
	assert max_astero_seen(grid_4) == (41, 6, 3)
	print("assert 4 OK")

	print(f"Result of first star is {max_astero_seen(grid)}")