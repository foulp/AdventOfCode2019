class Shuffle:
    def __init__(self, size_of_deck):
        self.deck_size = size_of_deck

    @staticmethod
    def cut(n):
        # f(x) = ax + b % deck_size, with a=1 and b=-n
        return 1, -n

    @staticmethod
    def deal_with_increment(n):
        # f(x) = ax + b % deck_size, with a=n and b=0
        return n, 0

    @staticmethod
    def deal_into_new_stack():
        # f(x) = ax + b % deck_size, with a=-1 and b=deck_size-1
        return -1, -1

    def full_shuffle(self, commands):
        # With f(x) = a'x + b' % deck_size, and g(x) = ax + b % deck_size
        # f(g(x)) = a'ax + (a'b + b') % deck_size
        a, b = 1, 0
        for technique in commands:
            if technique.startswith('deal with increment'):
                aa, bb = self.deal_with_increment(int(technique.split()[-1]))
            elif technique.startswith('cut'):
                aa, bb = self.cut(int(technique.split()[-1]))
            elif technique.startswith('deal into new stack'):
                aa, bb = self.deal_into_new_stack()
            else:
                raise ValueError(f"Did not understand command: {technique}")

            b = (bb + aa * b) % self.deck_size
            a = (a * aa) % self.deck_size
        return a, b


if __name__ == '__main__':
    with open('../inputs/Day22_input.txt', 'r') as f:
        commands_list = f.read().split('\n')

    deck_size = 10007
    start_pos = 2019
    shuffle = Shuffle(deck_size)
    a, b = shuffle.full_shuffle(commands_list)
    answer = (a * start_pos + b) % deck_size
    print(f"The result of first star is {answer}")
    # Solve a*x+b = end_pos [deck_size]
    # => a*x = (end_pos-b) [deck_size]
    # => x = (end_pos-b) * inv_mod(a, deck_size) [deck_size] if GCD(a, deck_size) == 1
    assert (answer - b) * pow(a, deck_size-2, deck_size) % deck_size

    n_turns = 101741582076661
    deck_size = 119315717514047
    end_pos = 2020
    already_met = [(a, b)]
    for _ in range(n_turns-1):
        b = (b + a * b) % deck_size
        a = (a * a) % deck_size
        if (a, b) in already_met:
            break
        else:
            already_met.append((a, b))

    a_final, b_final = already_met[n_turns % len(already_met)]
    print(a_final, b_final)
    answer = (end_pos - b_final) * pow(a_final, deck_size-2, deck_size) % deck_size
    print(f"The result of second star is {answer}")
