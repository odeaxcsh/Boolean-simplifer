from itertools import product
from main import to_sop_form

def margins_generator():
	i = 0.02
	while True:
		yield i
		i += 0.05
			
def rainbow_text(x,y,ls,lc,**kw):
    mls = map(lambda i: ls[i//2] if i%2 == 0 else '+', range(2*len(ls) - 1))
    mlc = map(lambda i: lc[i//2] if i%2 == 0 else 'k', range(2*len(lc) - 1))
    
    t = plt.gca().transData

    for s,c in zip(mls,mlc):
        text = plt.text(x,y, s,color=c, transform=t, **kw)
        text.draw(plt.gcf().canvas.get_renderer())
        t = transforms.offset_copy(text._transform, x=text.get_window_extent().width, units='dots')

def _decode(tuple):
	value = [0, 1, 2]
	return sum(3**i * value[v] for i, v in enumerate(tuple))

def _get_coord(list, margin):
	map = [((0, 1),), ((1, 1),), ((0, 2),), ((3, 1),), ((2, 1),), ((2, 2),), ((3, 1), (0, 1)), ((1, 2),), ((0, 4),)]
	if _decode(list) == 6:
		mg = [[margin, 0.1], [-0.1, -margin+0.1]]
	else: mg = [margin, -2*margin]
	return np.array(map[_decode(list)], dtype='float') + mg

def _draw_square(square, dim, margins, color, width):
	vnrow, vncol = dim
	rows, columns = square[vncol:], square[:vncol]
	
	nrow, ncol = 2**vnrow, 2**vncol
	
	xs = _get_coord(columns, margins)
	ys = _get_coord(rows, margins)
	
	for x, y in product(xs, ys):
		plt.gca().add_patch(Rectangle((x[0], nrow - y[0] - y[1]), x[1], y[1], edgecolor=color, facecolor=color+'30'))

def create_labels(x, y):
	if x is None and y is None:
		return []
	elif y is None:
		return [str(x) + "'", str(x)]
	else:
		return [f.format(str(y), str(x)) for f in ["{}'{}'", "{}'{}", "{}{}", "{}{}'"]]

def _at(vector, i):
	if i < len(vector):
		return vector[i]
	else: None

def draw_table(ones, squares, variables):
	plt.clf()
	plt.axis('off')
	vars_num = len(variables)
	if vars_num >= 5:
		raise ValueError('Number of variables > 4')

	colors = ['#A00000', '#00A000', '#0000A0', '#80FF80', '#FF00FF', '#FF8080', '#A0A000', '#202020', '#602080', "#800000"]

	nrow, ncol = dim_map[vars_num]
	rainbow_text(0, -0.125*nrow, to_sop_form(squares, variables).split('+'), colors, size=25)

	table = np.array(['1' if table_map(vars_num)[i] in ones else '0' for i in range(2**vars_num)]).reshape(dim_map[vars_num])

	dim = (vars_num//2, vars_num//2 + vars_num%2)
	c, r = variables[:dim[1]], variables[dim[1]:]

	col_labels = create_labels(_at(c, 0), _at(c, 1))
	row_labels = create_labels(_at(r, 0), _at(r, 1))

	plt.plot(np.tile([0, ncol], (nrow+1,1)).T, np.tile(np.arange(nrow+1), (2,1)), 'k', linewidth=3)
	plt.plot(np.tile(np.arange(0, ncol+1), (2,1)), np.tile([0, nrow], (ncol+1,1)).T, 'k', linewidth=3)

	for icol, col in enumerate(col_labels):
		plt.text(icol + 0.5, nrow+ 0.15, col, ha='center', va='center')
	for irow, row in enumerate(row_labels):
		plt.text(-0.15, nrow - irow - 0.5, row, ha='center', va='center')

	for irow, row in enumerate(table):
	    for icol, cell in enumerate(row):
	        plt.text(icol + 0.5, nrow - irow - 0.5, cell, ha='center', va='center')

	mg = margins_generator()
	for i, square in enumerate(squares):
		_draw_square(square, dim, next(mg), colors[i], 3)

	plt.show()
	plt.pause(0.0001)

def save_file(path):
	plt.savefig("imgs/" + path + ".png")

def init():
	from matplotlib.patches import Rectangle
	from matplotlib import transforms
	import matplotlib.pyplot as plt
	import numpy as np
	
	global plt, np, Rectangle, transforms
	global table_map, dim_map
	
	dim_map = [ (1, 1), (1, 2), (2, 2), (2, 4), (4, 4) ]
	
	_table_map = [
	[0], [0, 1], [0, 1, 2, 3],
	[0, 1, 3, 2, 4, 5, 7, 6],
	[0, 1, 3, 2, 4, 5, 7, 6, 12, 13, 15, 14, 8, 9, 11, 10] ]
	
	table_map = lambda index: _table_map[index] if index <= 4 else _table_map[4]