import csv

from file_reading.read_symmetric_relations import read_symmetric_relations

file = 'refined_domain_range.csv'
symm_file = 'symmetric_relations.txt'


def read_domain_range(file_name, symm_file):
	"""Reads the inputs and ranges of each relation type from the file where they are stored.
	:param file_name: the file where the domains and ranges are stored
	:param symm_file: the files containing the list of symmetric relations in the knowledge graph
	:returns: 
		(set) the relations in the knowledge graph
		(dict) the input types for each relation, keyed by relation to give the set of inputs
		(dict) the range types for each relation, keyed by relation to give the set of ranges
	"""
	rels = set()
	inputs = {}
	ranges = {}
	symmetric_relations = read_symmetric_relations(symm_file)

	with open(file_name, mode='r') as input_file:
		reader = csv.reader(input_file, delimiter=',', lineterminator='\r')
		header = True

		for row in reader:
			if header:
				header = False
				continue

			r, rel_input, input_range = row
			input_range = input_range.split(',')

			if r not in ranges.keys():
				ranges[r] = {}

			if rel_input not in ranges[r].keys():
				ranges[r][rel_input] = set()

			ranges[r][rel_input].update(set(input_range))  # = input_range  # .update(set(y))

			if r in symmetric_relations:
				for o in input_range:
					if o not in ranges[r].keys():
						ranges[r][o] = set()

				for o in input_range:
					ranges[r][o].update(rel_input)

	rels = list(ranges.keys())
	for r in ranges.keys():
		inputs[r] = list(ranges[r].keys())

	return rels, inputs, ranges

def read_domain_range_2(file_name, symm_file):
	"""Reads the inputs and input-specific ranges of each relation type from the file where they are stored.
	:param file_name: the file where the domains and ranges are stored
	:param symm_file: the files containing the list of symmetric relations in the knowledge graph
	:returns: 
		(set) the relations in the knowledge graph
		(dict) the input types for each relation, keyed by relation to give the set of inputs
		(dict) the range types for each relation, keyed by relation and input type to give the set of ranges
	"""
	rels = set()
	inputs = {}
	ranges = {}
	symmetric_relations = read_symmetric_relations(symm_file)

	with open(file_name, mode='r') as input_file:
		reader = csv.reader(input_file, delimiter=',', lineterminator='\r')
		header = True

		for row in reader:
			if header:
				header = False
				continue

			r, rel_input, input_range = row
			input_range = input_range.split(';')

			if r not in ranges.keys():
				ranges[r] = {}

			if rel_input not in ranges[r].keys():
				ranges[r][rel_input] = set()

			ranges[r][rel_input].update(set(input_range))  # = input_range  # .update(set(y))

			if r in symmetric_relations:
				for o in input_range:
					if o not in ranges[r].keys():
						ranges[r][o] = set()

				for o in input_range:
					ranges[r][o].update(rel_input)

	rels = sorted(list(ranges.keys()))
	for r in ranges.keys():
		inputs[r] = sorted(list(ranges[r].keys()))

	return rels, inputs, ranges

def read_entity_domain_range(file_name):
	"""Reads the domains and ranges of each relation type from the file where they are stored.
	:param file_name: the file where the domains and ranges are stored
	:returns: 
		(set) the relations in the knowledge graph
		(dict) the input entities for each relation, keyed by relation to give the set of inputs
		(dict) the range entities for each relation, keyed by relation to give the set of ranges
	"""
	rels = []
	domains = {}
	ranges = {}

	with open(file_name, 'r') as f:
		f.readline()
		for line in f:
			r, rel_domain, rel_range = line.split('\t')
			rels.append(r)
			domains[r] = rel_domain.split(',')
			ranges[r] = rel_range.split(',')

	return rels, domains, ranges



if __name__ == '__main__':
	rels, domains, ranges = read_domain_range(file, symm_file)
	print(rels)
	print('\n\n')
	for r in rels:
		print(r)
		print(ranges[r])
