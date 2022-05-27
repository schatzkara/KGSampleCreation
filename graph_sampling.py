import random
from file_reading.read_graph_txt import read_graph_txt
from file_reading.read_entities import read_entities
from file_reading.read_relations import read_relations

def random_walk(input_file, output_file, desired_size, rels_to_avoid=[], entities_to_avoid=[], restart_prob=15, verbose=True):
	# print(entities_to_avoid)
	# print(rels_to_avoid)

	nodes, _, _, graph = read_graph_txt(input_file)
	if verbose:
		print('read graph')
	graph_size = calculate_graph_size(graph)
	if verbose:
		print('got graph size: {}'.format(graph_size))
	sample = set()

	previous_size = 0
	while len(sample) < desired_size:
		start_node = random.choice(list(graph.keys()))  

		while start_node in entities_to_avoid:
			start_node = random.choice(list(graph.keys()))

		current_node = start_node
		
		count = 0
		while count < (100 * len(nodes)) and len(sample) < desired_size:
			if random.randint(0, 99) < restart_prob:
				current_node = start_node
				if start_node not in graph.keys():
					break

			if current_node in graph.keys():
				possible_paths = [(p, o) for p in graph[current_node].keys() for o in graph[current_node][p].keys()]

				if len(possible_paths) != 0:
					p, o = random.choice(possible_paths)

					if p not in rels_to_avoid and o not in entities_to_avoid:
						sample.add((current_node, p, o))

					# is this allowed??
					graph[current_node][p].pop(o)    
					if len(graph[current_node][p]) == 0:
						graph[current_node].pop(p)
					if len(graph[current_node]) == 0:
						graph.pop(current_node)
					current_node = o
				else:
					graph.pop(current_node)

			count += 1
			if verbose and len(sample) - previous_size >= 100000:
				print(len(sample))
				previous_size = len(sample)

	sample = sorted(list(sample), key=lambda x: (x[1], int(x[0]), int(x[2])))

	with open(output_file, 'w') as f:
		for s, p, o in sample:
			f.write('{}\t{}\t{}\n'.format(s, p, o))

def calculate_graph_size(graph):
	size = 0
	for s in graph.keys():
		for p in graph[s].keys():
			size += len(graph[s][p].keys())

	return size


if __name__ == '__main__':
	file_name = 'robokop_singular_symm_rels.txt'
	output_file = 'sample2.txt'
	rels_to_avoid = set(read_relations('data_files/robokop/ontological_relations.txt'))
	# rels_to_avoid.add('subclass_of')
	# rels_to_avoid.update(read_relations('data_files/robokop/non_prevalent_rels_1.txt'))
	# rels_to_avoid.remove('treats')
	entities_to_avoid = set(read_entities('data_files/robokop/ontological_entities.txt'))

	random_walk(file_name, output_file, desired_size=4000000, rels_to_avoid=rels_to_avoid, entities_to_avoid=entities_to_avoid)
