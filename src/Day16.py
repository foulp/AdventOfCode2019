def fft(inputs_list, n_phases, base_pattern=(0, 1, 0, -1), msg_offset=0, offset=1):
	inputs_list = list(map(int, inputs_list))
	for _ in range(n_phases):
		result = []
		for k in range(1, len(inputs_list)+1):
			m = 0
			for i, v in enumerate(inputs_list):
				val = v*base_pattern[((offset + i)//k) % len(base_pattern)]
				m += val
			result.append(abs(m) % 10)
		inputs_list = result[:]

	return ''.join(map(str, inputs_list[msg_offset: msg_offset+8]))


if __name__ == '__main__':
	with open('../inputs/Day16_input.txt', 'r') as f:
		n = f.read().strip()

	assert fft([1, 2, 3, 4, 5, 6, 7, 8], 4) == '01029498'
	print('Assert 1 OK')
	assert fft('80871224585914546619083218645595', 100) == '24176176'
	print('Assert 2 OK')
	assert fft('19617804207202209144916044189917', 100) == '73745418'
	print('Assert 3 OK')
	assert fft('69317163492948606335995924319873', 100) == '52432133'
	print('Assert 4 OK')

	print(f"The result of first star is {fft(n, 100)}")

	n1 = '03036732577212944063491565474664'
	assert fft(10000*n1, 100, msg_offset=int(n1[:7])) == '84462026'
	print('Assert 1 OK')
	n2 = '02935109699940807407585447034323'
	assert fft(10000*n2, 100, msg_offset=int(n2[:7])) == '78725270'
	print('Assert 2 OK')
	n3 = '03081770884921959731165446850517'
	assert fft(10000*n3, 100, msg_offset=int(n3[:7])) == '53553731'
	print('Assert 3 OK')

	print(f"The result of second star is {fft(10000*n, 100, msg_offset=int(n[:7]))}")