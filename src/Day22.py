class SpaceCard:
    def __init__(self, pos, size_of_deck):
        self.pos = pos
        self.deck_size = size_of_deck

    def cut(self, n):
        if n > 0:
            if n <= self.pos:
                self.pos -= n
            else:
                self.pos += self.deck_size - n
        else:
            if self.pos >= self.deck_size + n:
                self.pos -= self.deck_size + n
            else:
                self.pos -= n

    def deal_with_increment(self, n):
        self.pos = (self.pos * n) % self.deck_size

    def deal_into_new_stack(self):
        self.pos = self.deck_size - self.pos - 1

    def shuffle(self, commands):
        for technique in commands:
            if technique.startswith('deal with increment'):
                self.deal_with_increment(int(technique.split()[-1]))
            elif technique.startswith('cut'):
                self.cut(int(technique.split()[-1]))
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

# WRONG
    n_turns = 101741582076661
    deck_size = 119315717514047
    space_card = SpaceCard(2020, deck_size)
    already_met = [space_card.pos]
    for _ in range(n_turns):
        space_card.shuffle(commands_list)
        if space_card.pos not in already_met:
            already_met.append(space_card.pos)
        else:
            break

    answer = already_met[n_turns % len(already_met)]
    print(f"The result of second star is {answer}")
