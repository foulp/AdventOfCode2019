class SpaceCard:
    def __init__(self, pos, size_of_deck):
        self.pos = pos
        self.deck_size = size_of_deck

    def cut(self, n, order=1):
        self.pos = (self.pos - order * n) % self.deck_size

    def deal_with_increment(self, n, order=1):
        if order == 1:
            self.pos = (self.pos * n) % self.deck_size
        else:
            while self.pos % n:
                self.pos += self.deck_size
            self.pos //= n

    def deal_into_new_stack(self):
        self.pos = self.deck_size - self.pos - 1

    def shuffle(self, commands, order=1):
        for technique in commands[::order]:
            if technique.startswith('deal with increment'):
                self.deal_with_increment(int(technique.split()[-1]), order)
            elif technique.startswith('cut'):
                self.cut(int(technique.split()[-1]), order)
            elif technique.startswith('deal into new stack'):
                self.deal_into_new_stack()
            else:
                raise ValueError(f"Did not understand command: {technique}")


if __name__ == '__main__':
    with open('../inputs/Day22_input.txt', 'r') as f:
        commands_list = f.read().split('\n')

    space_card = SpaceCard(2019, 10007)
    space_card.shuffle(commands_list)
    print(f"The result of first star is {space_card.pos}")

    n_turns = 101741582076661
    deck_size = 119315717514047
    space_card = SpaceCard(2020, deck_size)
    already_met = [space_card.pos]
    for _ in range(n_turns):
        space_card.shuffle(commands_list, order=-1)
        if space_card.pos not in already_met:
            already_met.append(space_card.pos)
        else:
            break

    answer = already_met[n_turns % len(already_met)]
    print(f"The result of second star is {answer}")
