from src.lib.intcode import Amplifier


class Network:
    def __init__(self, n_computers, intcode):
        self.n_computers = n_computers
        self.computers = [Computer(i, intcode[:]) for i in range(n_computers)]
        self.nat = None
        self.last_nat = None

    def run(self, star):
        compte = 0
        while True:
            for i in range(self.n_computers):
                if self.computers[i].amp.run_short(default_input=-1) == 0 and not self.computers[i].amp.done:
                    self.computers[i].producted.append(self.computers[i].amp.value)
                    if len(self.computers[i].producted) == 3:
                        a, x, y = self.computers[i].producted
                        if a == 255:
                            if star == 1:
                                return y
                            else:
                                self.nat = [x, y]
                        else:
                            self.computers[a].amp.inputs.extend((x, y))
                        self.computers[i].producted = []

            if star == 2:
                if self.nat and all(self.computers[j].amp.inputs == [] for j in range(self.n_computers)):
                    self.computers[0].amp.inputs = self.nat
                    if self.nat[1] == self.last_nat:
                        return self.last_nat
                    self.last_nat = self.nat[1]


class Computer:
    def __init__(self, address, intcode):
        self.amp = Amplifier(intcode[:], address)
        self.address = address
        self.queue = []
        self.producted = []


if __name__ == '__main__':
    with open('../inputs/Day23_input.txt', 'r') as f:
        program = list(map(int, f.read().split(',')))

    network = Network(50, program[:])
    print(f"The result of first star is {network.run(star=1)}")
    network = Network(50, program[:])
    print(f"The result of second star is {network.run(star=2)}")
