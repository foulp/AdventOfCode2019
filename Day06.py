with open('Day06_input.txt', 'r') as f:
	orbits = f.read().split('\n')

#orbits = ['B)C', 'D)E', 'E)F', 'B)G', 'COM)B', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L', 'C)D']
orbits = ['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L', 'K)YOU', 'I)SAN']

planets = {}
for orb in [o for o in orbits if o!='']:
	p1, p2 = orb.split(')')
	if p2 == 'SAN':
		target = p1
	if p1 == 'YOU':
		source = p1
	if p1 in planets:
		planets[p1].add(p2)
		if p2 in planets: planets[p1].update(planets[p2])
	else:
		planets[p1] = set([p2])
		if p2 in planets: planets[p1].update(planets[p2])

	for p in planets:
		if p1 in planets[p]: 
			planets[p].add(p2)
			if p2 in planets: planets[p].update(planets[p2])

print(f"Result of first star is {sum(len(planets[p]) for p in planets)}")

print([(p, len(planets[p])) for p in planets if 'SAN' in planets[p] and 'YOU' in planets[p]])
father = min([(len(planets[p]), p) for p in planets if 'SAN' in planets[p] and 'YOU' in planets[p]])
print(father)