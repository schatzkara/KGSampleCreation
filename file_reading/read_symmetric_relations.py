def read_symmetric_relations(file):
	"""Reads the symmetric relations from the file in which they are stored.
	:param file: the file where the list of symmetric relations is stored
	:returns: (list) the symmetric relations in the knowledge graph
	"""
	with open(file, 'r') as f:
		symmetric_relations = f.read().strip().split('\n')
		symmetric_relations = [s.replace(' ', '_') for s in symmetric_relations]
		# print(symmetric_relations)

	return symmetric_relations


if __name__ == '__main__':
	file = 'symmetric_relations.txt'
	read_symmetric_relations(file)
