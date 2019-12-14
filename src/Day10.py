import numpy as np

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

def asteros_seen(rows, cols, i, j, epsilon):
	a = Point(rows[i], cols[i])
	b = Point(rows[j], cols[j])

	for k in range(i+1, j):
		c = Point(rows[k], cols[k])
		crossproduct = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)
		if abs(crossproduct) <= epsilon:
			return False
	return True

def max_astero_seen(grid, epsilon=0):
	rows, cols = np.where(grid == '#')
	sights = np.zeros((rows.shape[0], rows.shape[0]))
	for i in range(rows.shape[0]):
		for j in range(i+1, cols.shape[0]):
			if asteros_seen(rows, cols, i, j, epsilon):
				sights[i, j] = sights[j, i] = 1
	return max((v, cols[i], rows[i]) for i, v in enumerate(sights.sum(axis=1)))

def vaporized(grid, location, n=200):
	station_y, station_x = location
	grid[station_x, station_y] = 'X'
	rows, cols = np.where(grid=='#')
	c = 0
	angles = [[np.angle((x-station_x) + (y-station_y)*1j, deg=True), -(x-station_x)**2-(y-station_y)**2, x, y] for x,y in zip(rows, cols)]
	angles.sort(reverse=True)
	#print(angles)
	for i in range(len(angles)-1):
		j, k = 1, 1
		while angles[i][0] == angles[i+j][0]:
			angles[i+j][0] -= k*360
			k += 1
			j += 1

	return sorted(angles, reverse=True)[n-1][2:]

if __name__ == '__main__':
	with open('../inputs/Day10_input.txt', 'r') as f:
		grid = np.array([[c for c in line] for line in f.read().strip().split('\n')])

	grid_1 = np.array(list('.#..#.....#####....#...##')).reshape(5, 5)
	
	grid_2 = np.array(list('......#.#.#..#.#......#######..#.#.###...#..#.......#....#.##..#....#..##.#..#####...#..#..#....####'))
	grid_2 = grid_2.reshape(10, 10)
	
	grid_3 = np.array(list('#.#...#.#..###....#..#....#...##.#.#.#.#....#.#.#..##..###.#..#...##....##....##......#....####.###.'))
	grid_3 = grid_3.reshape(10, 10)

	grid_4 = np.array(list('.#..#..#######.###.#....###.#...###.##.###.##.#.#.....###..#..#.#..#.##..#.#.###.##...##.#.....#.#..'))
	grid_4 = grid_4.reshape(10, 10)

	s = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""
	grid_5 = np.array([[c for c in line] for line in s.split('\n')])

	assert max_astero_seen(grid_1) == (8, 3, 4)
	print("assert 1 OK")
	assert max_astero_seen(grid_2) == (33, 5, 8) 
	print("assert 2 OK")
	assert max_astero_seen(grid_3) == (35, 1, 2)
	print("assert 3 OK")
	assert max_astero_seen(grid_4) == (41, 6, 3)
	print("assert 4 OK")
	assert max_astero_seen(grid_5) == (210, 11, 13)
	print("assert 5 OK")

	location = max_astero_seen(grid)
	print(f"Result of first star is {location[0]}")

	assert vaporized(grid_5, (11, 13), 1) == [12, 11]
	assert vaporized(grid_5, (11, 13), 2) == [1, 12]
	assert vaporized(grid_5, (11, 13), 3) == [2, 12]
	assert vaporized(grid_5, (11, 13), 10) == [8, 12]
	assert vaporized(grid_5, (11, 13), 20) == [0, 16]
	assert vaporized(grid_5, (11, 13), 50) == [9, 16]
	assert vaporized(grid_5, (11, 13), 100) == [16, 10]
	assert vaporized(grid_5, (11, 13), 199) == [6, 9]
	assert vaporized(grid_5, (11, 13), 200) == [2, 8]
	assert vaporized(grid_5, (11, 13), 201) == [9, 10]
	assert vaporized(grid_5, (11, 13), 299) == [1, 11]

	y, x = vaporized(grid, location[1:], 200)
	print(f"Result of second star is {100*x+y}")