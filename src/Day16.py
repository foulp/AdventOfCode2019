def fft(inputs_list, n_phases, base_pattern=[0, 1, 0, -1], offset=1):
	inputs_list = list(map(int, inputs_list))
	for _ in range(n_phases):
		result = []
		for k in range(1, len(n)+1):
			m = 0
			for i, v in enumerate(inputs_list):
				val = v*base_pattern[((offset + i)//k)%len(base_pattern)]
				m += val
			result.append(abs(m)%10)
		inputs_list = result[:]

	return ''.join(map(str, result[:8]))


if __name__ == '__main__':
	with open('Day16_input.txt', 'r') as f:
		n = f.read().strip()

	assert fft([1,2,3,4,5,6,7,8], 4) == '01029498'
	print('Assert 1 OK')
	assert fft('80871224585914546619083218645595', 100) == '24176176'
	print('Assert 2 OK')
	assert fft('19617804207202209144916044189917', 100) == '73745418'
	print('Assert 3 OK')
	assert fft('69317163492948606335995924319873', 100) == '52432133'
	print('Assert 4 OK')


	print(f"The result of first star is {fft(n, 100)}")