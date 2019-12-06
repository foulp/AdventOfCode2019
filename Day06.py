with open('Day06_input.txt', 'r') as f:
	orbits = f.read().split('\n')

planets = {}
fathers = {}
for orb in [o for o in orbits if o!='']:
	p1, p2 = orb.split(')')
	fathers[p2] = p1
	if p2 == 'SAN':
		target = p1
	if p2 == 'YOU':
		source = p1
	planets[p1] = planets.get(p1, []) + [p2]
	if p2 in planets:
		planets[p1].extend(planets[p2])

	for p in planets:
		if p1 in planets[p]: 
			planets[p].append(p2)
			if p2 in planets:
				planets[p].extend(planets[p2])

print(f"Result of first star is {sum(len(planets[p]) for p in planets)}")

commun = min((p for p in planets if 'SAN' in planets[p] and 'YOU' in planets[p]), key=lambda p: len(planets[p]))
c = 0
while source != commun:
	c += 1
	source = fathers[source]
while target != commun:
	c += 1
	target = fathers[target]
print(f"Result of second star is {c}")
