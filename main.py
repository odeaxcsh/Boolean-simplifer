from Parser import parse_logical_expression as parse
from karnaugh_algorithm import simplify
from datetime import datetime

def graphics_init():
	from graphics import draw_table, save_file, init
	global draw_table, save_file
	init()
	
def to_sop_form(terms, variables):
	terms_str = []
	sign_map = { -1 : "", 0 : "{}'", 1 : "{}" }
	for term in terms:
		term_expr = [sign_map[t].format(str(v)) for t, v in zip(term, variables)]
		term_str = "".join(sorted(term_expr))
		if term_str == "":
			terms_str.append('1')
		else: terms_str.append(term_str)
	return "+".join(terms_str) if terms else '0'
	
def args_val(vars):
	return sum([2**i * p.get_value() for i, p in enumerate(vars)])

def _sort(vars):
	vars.sort(key=lambda x: ord(str(x)))
	i = 0
	if len(vars) != 2:
		while i < len(vars)-1:
			vars[i], vars[i+1] = vars[i+1], vars[i]
			i += 2
	return vars

def get_func(string):
	string = string.split()
	vars, ones = [], []
	i = 0
	while i < len(string):
		if 'a' <= string[i] <= 'z' or 'A' <= string[i] <= 'Z':
			vars.append(string[i])
		else: break
		i += 1
	
	while i < len(string):
		ones.append(int(string[i]))
		i += 1
	
	return vars, ones
	
def main():
	input_mode = 1
	graphics_on = False
	graphics_virgin = True

	while True:
		string = input("[In]: ")

		if string[0:1] == '-':
			command = string[1:].lower().split()
			if not command: command = ['']
			if command[0] == 'exit':
				break
			elif command[0] == 'input-mode':
				try:
					if command[1] == 'expression':
						input_mode = 1
					elif command[1] == 'function':
						input_mode = 0
					else:
						print('[Cmd]: input-mode usage: -INPUT-MODE <EXPRESSION/FUNCTION>')
				except IndexError:
					print('[Cmd]: input-mode usage: -INPUT-MODE <EXPRESSION/FUNCTION>')

			elif command[0] == 'graphics':
				try:
					if command[1] == 'on':
						graphics_on = True
					elif command[1] == 'off':
						graphics_on = False
					else:
						print('[Cmd]: graphics command usage: -GRAPHICS <ON/OFF>')
				except IndexError:
					print('[Cmd]: graphics command usage: -GRAPHICS <ON/OFF>')
			else:
				print("[Cmd]: invalid command")
				
			if graphics_virgin and graphics_on:
				graphics_virgin = False
				try:
					graphics_init()
				except Exception as e:
					graphics_virgin = True
					print('[Graphics initializer]:', str(e))
			continue
			
		try:
			if input_mode == 1:
				string = "".join(string.split())
				expr, vars = parse(string)
				vars = _sort(list(vars.values()))
				ones = [ args_val(vars) for p in expr.eval() if p ]
			else:
				try:
					vars, ones = get_func(string)
					vars.reverse()
				except:
					print("[Out]: invalid input")

			reduced = simplify(ones, len(vars))
			print("[Out]:", to_sop_form(reduced, vars))
			if graphics_on:
				try:
					draw_table(ones, reduced, list(vars))
					save_file(("expr-" if input_mode else "func-") + str(datetime.now()))
				except Exception as e:
					print('[Graphics]:', str(e))

		except Exception as e:
			print('[Parser]:', str(e))

if __name__ == '__main__':
	main()