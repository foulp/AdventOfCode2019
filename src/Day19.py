import numpy as np
from src.lib.intcode import Amplifier


if __name__ == '__main__':
    with open('../inputs/Day19_input.txt', 'r') as f:
        program = list(map(int, f.read().split(',')))

    compteur = 0
    for i in range(50):
        for j in range(50):
            amp = Amplifier(program[:])
            value = amp.run(values=[i, j])
            if value == 1:
                compteur += 1
    print(f"The result of first star is {compteur}")

    x, y = 4, 3  # First angle of the beam, beam is empty between (0, 0) and (4, 3)
    size = 100
    while True:
        value = Amplifier(program[:]).run(values=[x+size-1, y])
        if value == 1:
            value = Amplifier(program[:]).run(values=[x, y+size-1])
            if value == 1:
                break
            else:
                x += 1
        else:
            y += 1

    print(f"The result of second star is {10000 * x + y}")
