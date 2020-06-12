import numpy as np


def gen_col(k, size, base_pattern=(0, 1, 0, -1)):
	column = np.repeat(base_pattern, k)
	column = np.pad(column, (0, max(0, size + 1 - column.shape[0])), mode='wrap')
	column = np.delete(column, 0)
	return np.delete(column, np.s_[size:])


def fft(inputs_list, n_phases, base_pattern=(0, 1, 0, -1), msg_offset=0):
	inputs_list = np.array(list(map(int, inputs_list)))
	length = inputs_list.shape[0]
	array = gen_col(1, length, base_pattern)
	for k in range(2, length+1):
		array = np.column_stack((array, gen_col(k, length)))
	for _ in range(n_phases):
		inputs_list = abs(np.dot(inputs_list, array)) % 10

	return ''.join(map(str, inputs_list[msg_offset: msg_offset+8]))


def fft_v2(inputs_list, n_phases):
	""" If the offset is bigger than half the inputs length,"""
	""" then we can only work with the digits starting at the offset. Which is always the case """
	""" Because the pattern then is only a lower triangular matrix filled with ones """
	""" Hence the use of the cumsum """
	offset = int(inputs_list[:7])
	message = np.array(list(map(int, (10000 * inputs_list)[offset:])))
	length = len(message)
	assert length <= 10000*len(inputs_list) / 2
	for _ in range(n_phases):
		message[::-1] = abs(message[::-1].cumsum()) % 10
	return ''.join(map(str, message[:8]))


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
	assert fft_v2(n1, 100) == '84462026'
	print('Assert 1 OK')
	n2 = '02935109699940807407585447034323'
	assert fft_v2(n2, 100) == '78725270'
	print('Assert 2 OK')
	n3 = '03081770884921959731165446850517'
	assert fft_v2(n3, 100) == '53553731'
	print('Assert 3 OK')

	print(f"The result of second star is {fft_v2(n, 100)}")