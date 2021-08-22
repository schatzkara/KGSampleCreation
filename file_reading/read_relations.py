def read_relations(file):
	"""Reads the relations from the file in which they are stored.
	:param file: the file where the list of relations is stored
	:returns: (list) the relations in the knowledge graph
	"""
	with open(file, 'r') as f:
		relations = f.read().strip().split('\n')
		relations = [r.replace(' ', '_') for r in relations]

	return relations


if __name__ == '__main__':
	file = 'ontological_relations.txt'
	read_ontological_relations(file)
