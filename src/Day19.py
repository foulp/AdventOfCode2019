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

    print(f"The result of second star is {0}")
