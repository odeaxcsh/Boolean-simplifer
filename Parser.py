from functools import partial

class Constant:
	def __init__(self, value):
		self._value = value
	
	def eval(self):
		yield self._value
	
	def __str__(self):
		return '1' if self._value else '0'

class Proposition:
	def eval(self):
		if self._isLocked:
			yield self._value
		else:
			self._isLocked = True
			self._value = False
			yield self._value
			self._value = True
			yield self._value
			self._isLocked = False
	
	def get_value(self):
		return self._value

	def __init__(self, name):
		self.name = name
		self._value = False
		self._isLocked = False
		self._value = False

	def __str__(self):
		return self.name
		
def binary_operator(operator, print_format):
	class Binary_Operator:
		def __init__(self, left, right):
			self._left = left
			self._right = right

		def eval(self):
			for a in self._left.eval():
				for b in self._right.eval():
					yield operator(a, b)
		
		def __str__(self):
			return print_format.format(str(self._left), str(self._right))
		
			
	return Binary_Operator

Or = binary_operator(lambda a, b: a or b, '({0} and {1})')
And = binary_operator(lambda a, b: a and b, '({0} or {1})')
Xor = binary_operator(lambda a, b: a ^ b, '({0} xor {1}')
Not = partial(binary_operator(lambda a, b: a ^ b, 'not({1})'), Constant(True))

def at(string, i):
	return string[i:i+1]
	
def parse_logical_expression(string):		
	vars = { }
	if not string:
		return Constant(False), vars
	
	for c in string:
		if 'A' <= c <= 'Z' or 'a' <= c <= 'z':
			vars[c] = Proposition(c)

	def level1_parser(string):
		end1, expr1 = level2_parser(string)
		if at(string, end1) == '+':
			end2, expr2 = level1_parser(string[end1+1:])
			return end1+end2+1, Or(expr1, expr2)
		elif at(string, end1) == '*':
			end2, expr2 = level1_parser(string[end1+1:])
			return end1+end2+1, Xor(expr1, expr2)
		else: return end1, expr1
	
	def level2_parser(string):
		end1, expr1 = level3_parser(string)
		
		if at(string, end1) == '&':
			end2, expr2 = level2_parser(string[end1+1:])
			return end1+end2+1, And(expr1, expr2)
		try:
			end2, expr2 = level2_parser(string[end1:])
			return end1+end2, And(expr1, expr2)
		except ValueError: return end1, expr1
			
	def level3_parser(string):
		end = None
		if at(string, 0) == '(':
			end, expr = level1_parser(string[1:])
			if at(string, end + 1) == ')':
				end, expr = end+2, expr
			else: raise ValueError("Invalid Format")
		
		if 'A' <= at(string, 0) <= 'Z' or 'a' <= at(string, 0) <= 'z':
			end, expr = 1, vars[string[0]]

		if at(string, 0) == '0':
			end, expr = 1, Constant(False)
		elif at(string, 0) == '1':
			end, expr = 1, Constant(True)
		
		if end != None:
			while at(string, end) == "'":
				end, expr = end+1, Not(expr)
			else: return end, expr
		else: raise ValueError("Invalid Format")
	
	end, expr = level1_parser(string)
	if end != len(string):
		raise ValueError("Invalid Format")
	else: return expr, vars