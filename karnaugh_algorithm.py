def generate_ones(term, ones):
	sum = 0
	def _generate_ones(i):
		nonlocal sum
		if i == len(term):
			if sum not in ones:
				ones.add(sum)
			return
		if term[i] in [1, -1]:
			sum += 2**i
			_generate_ones(i+1)
			sum -= 2**i
		if term[i] in [0, -1]:
			_generate_ones(i+1)
	_generate_ones(0)
	return ones

def reduce(squares):
	for i in range(len(squares)):
		this, others = set(), set()
		generate_ones(squares[i], this)
		for j in range(len(squares)):
			if j != i:
				generate_ones(squares[j], others)

		if this < others:
			del squares[i]

def extend_squares(ones, matches_length):
	should_del = []

	for i in range(len(ones)):
		for j in range(i+1, len(ones)):
			matches = [i == j for i, j in zip(ones[i], ones[j])]
			if(sum(matches) == matches_length):
				ones.append([k if matched else -1 for k, matched in zip(ones[i], matches)])
				should_del.append(i)
				should_del.append(j)

	output = []
	for i in range(len(ones)):
		if i not in should_del and ones[i] not in output:
			output.append(ones[i])
	return output

def simplify(ones, length):
	
	ones_in_binary = [ [int(digit) for digit in format(num, 'b').zfill(length)[::-1]] for num in ones]
	extended_ones = ones_in_binary
	
	for _ in range(length):
		extended_ones = extend_squares(extended_ones, length-1)
	
	reduce(extended_ones)
	
	return extended_ones