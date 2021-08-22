def read_type_hierarchy(file_name):
	"""Reads the entity type hierarchy from the file in which it is stored.
	:param file_name: the file where the entity type hierarchy is stored
	:returns: 
		(dict) the type hierarchy keyed by each child to access its parent
		(dict) the type hierarchy keyed by each parent to access its list of children
	"""
	parents = {}
	children = {}

	with open(file_name, 'r') as f:
		for line in f:
			line = line.strip().split('\t')
			# print(len(line))
			if len(line) == 3:
				t, p, c = line  # .strip().split('\t')
				c = c.split(',')
				# parents[t] = p
				# children[t] = c.split(',')
				# children = children.split(',')
			elif len(line) == 2:
				t, p = line  # .strip().split('\t')
				c = []
				# parents[t] = p
				# children[t] = []
				# children = []
			elif len(line) == 1:
				t = line[0]
				p = None
				c = []
			else: 
				print("ERROR")
				quit()

			# print(p)
			# if p == 'None':
				# print('here')
			# print(t)
			# print(p)
			# print(c)
			parents[t] = p if p != 'None' else None
			children[t] = c
			# type_hierarchy[parent] = children

	return parents, children


if __name__ == '__main__':
	file_name = 'data_files/type_hierarchy.txt'
	hierarchy = read_type_hierarchy(file_name)
	print(hierarchy)
