def read_entities(file):
	"""Reads the entities from the file in which they are stored.
	:param file: the file where the list of entities is stored
	:returns: (list) the entities in the knowledge graph
	"""
	with open(file, 'r') as f:
		entities = f.read().strip().split('\n')
		entities = [int(r) for r in entities]

	return entities


if __name__ == '__main__':
	file = 'ontological_entities.txt'
	read_entities(file)
