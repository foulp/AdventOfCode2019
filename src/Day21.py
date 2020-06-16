from src.lib.intcode import Amplifier
from src.Day17 import commands_to_ascii


def run_commands(commands):
    amp = Amplifier(program[:])
    line = ''
    while amp.done is False:
        case = amp.run()
        if amp.done:
            break
        if case == ord('\n'):
            print(line)
            if line == 'Input instructions:':
                for c in commands:
                    amp.inputs.extend(c)
            line = ''
            continue
        try:
            line += chr(case)
        except Exception as e:
            print(e)

    return amp.value


if __name__ == '__main__':
    with open('../inputs/Day21_input.txt', 'r') as f:
        program = list(map(int, f.read().split(',')))

    commands = commands_to_ascii(["NOT A J", "NOT B T", "OR T J", "NOT C T", "OR T J", "AND D J", "WALK"])

    print(f"The result of first star is {run_commands(commands)}")

    commands = commands_to_ascii(["NOT A J", "NOT B T", "OR T J", "NOT C T", "OR T J", "AND D J", "RUN"])

    print(f"The result of second star is {run_commands(commands)}")
