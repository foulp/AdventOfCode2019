import matplotlib.pyplot as plt
import numpy as np

with open('../inputs/Day08_input.txt', 'r') as f:
	image = f.read().strip()

n = 25 * 6
layers = [image[i:i + n] for i in range(0, len(image), n)]

target = min([layer for layer in layers], key=lambda l: l.count('0'))
print(f"The result of first star is {target.count('1') * target.count('2')}")

r = []

for j in range(6):
	for i in range(25):
		pixel = [l[i+25*j] for l in layers]
		r.append(next((int(p) for p in pixel if p!='2')))

plt.imshow(np.array(r).reshape(6,25), cmap=plt.cm.gray)
plt.show()
