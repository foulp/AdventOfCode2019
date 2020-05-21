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
        full_a, full_b = 1, 0
        for technique in commands:
            if technique.startswith('deal with increment'):
                aa, bb = self.deal_with_increment(int(technique.split()[-1]))
            elif technique.startswith('cut'):
                aa, bb = self.cut(int(technique.split()[-1]))
            elif technique.startswith('deal into new stack'):
                aa, bb = self.deal_into_new_stack()
            else:
                raise ValueError(f"Did not understand command: {technique}")

            full_b = (bb + aa * full_b) % self.deck_size
            full_a = (full_a * aa) % self.deck_size
        return full_a, full_b


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
    # NB : inv_mod(a, m) is x in range(0, m) such that a*x = 1 [m], exists iff GCD(a, m) = 1
    # NB : inv_mod(a, deck_size) = pow(a, deck_size-2, deck_size) valid iff deck_size is prime
    assert start_pos == (answer - b) * pow(a, deck_size-2, deck_size) % deck_size

    n_turns = 101741582076661
    deck_size = 119315717514047
    end_pos = 2020
    shuffle = Shuffle(deck_size)
    a, b = shuffle.full_shuffle(commands_list)
    # f^-1(x) = inv_mod(a, deck_size) * (x-b) % deck_size
    # f^n(x) = a**n * x + b * (1 + a + a**2 + a**3 + ... + a**(n-1)) % deck_size
    a_final = pow(a, n_turns, deck_size)
    b_final = b * (pow(a, n_turns, deck_size) - 1) * pow(a-1, deck_size-2, deck_size) % deck_size

    answer = (end_pos - b_final) * pow(a_final, deck_size-2, deck_size) % deck_size
    print(f"The result of second star is {answer}")
