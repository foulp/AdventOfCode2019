day04_input = range(138307, 654504 + 1)

def correct_pw(i):
	str_i = str(i)
	good = False
	for j, d in enumerate(str_i[:-1]):
		if d == str_i[j+1]:
			good = True
		elif d > str_i[j+1]:
			return False
	return good

assert correct_pw(111111) == True
assert correct_pw(223450) == False
assert correct_pw(123456) == False

c = sum(correct_pw(i) for i in day04_input)
print(f"The result of first star is {c}")

def new_correct_pw(i):
	str_i = str(i)
	good = False
	for j, d in enumerate(str_i[:-1]):
		if d == str_i[j+1] and (j+2==len(str_i) or d!=str_i[j+2]) and (j==0 or d!=str_i[j-1]):
			good = True
		elif d > str_i[j+1]:
			return False
	return good

assert new_correct_pw(112233) == True
assert new_correct_pw(123444) == False
assert new_correct_pw(111122) == True

c = sum(new_correct_pw(i) for i in day04_input)
print(f"The result of second star is {c}")
