from src.lib.intcode import Amplifier

if __name__ == '__main__':
    with open('../inputs/Day25_input.txt', 'r') as f:
        program = list(map(int, f.read().split(',')))

    amp = Amplifier(program[:])
    line = ''
    while amp.done is False:
        case = amp.run()
        if case == ord('\n'):
            print(line)
            if line == 'Command?':
                amp.inputs.extend(list(map(ord, input("Type command") + '\n')))
            line = ''
            continue
        line += chr(case)

    # 					        SICK BAY
    # KITCHEN (infinite loop)	PASSAGES (astrolabe)	HOT CHOCOLATE FOUTAIN	ENGINEERING (escape pod)	NAVIGATION (coin)	            STORAGE (molten lava)
    # HOLODECK			                                                        HULL BREACH	CORRIDOR (cake)	GIFT WRAPPING CENTER (photons)	OBSERVATORY (giant electromagnet)	SECURITY CHECKPOINT
    # WARP DRIVE MAINTENANCE (sand)			ARCADE (food ration)	HALLWAY (weather machine)			                                                                        PRESSURE SENSITIVE FLOOR
    # 		CREW QUARTERS (jam)	            SCIENCE LAB (ornament)	STABLES
    # Food ration Astrolabe, Ornament, Weather machine is needed for the weight correction
    print(f"The result of second star is {0}")
