def draw_path(string):
	points = []
	x = 0
	y = 0
	for direction in string.split(','):
		d, n = direction[0], int(direction[1:])
		for _ in range(n):
			if d == 'R':
				x += 1
			elif d == 'L':
				x -= 1
			elif d == 'U':
				y += 1
			elif d == 'D':
				y -= 1
			points.append((x,y))

	return points

def find_cross(l1, l2):
	return set(l1).intersection(l2)

def closest_point(crosses):
	return min(abs(a) + abs(b) for a, b in crosses)

with open('Day03_input.txt', 'r') as f:
	lines = [draw_path(string) for string in f]

crosses = find_cross(lines[0], lines[1])
print(f"The result of first star is {closest_point(crosses)}")

travel_dist = min(2 + lines[0].index(p) + lines[1].index(p) for p in crosses)
print(f"The result of second star is {travel_dist}")