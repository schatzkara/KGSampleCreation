
def read_graph_txt(file_name, types_file=None):
	nodes = set()
	predicates = set()
	triples = []
	graph = {}
	with open(file_name, 'r') as f:
		for line in f:
			s, p, o = line.strip().split('\t')
			s, o = int(s), int(o)
			# add nodes
			nodes.add(s)
			nodes.add(o)
			# add predicate
			predicates.add(p)
			# add triple
			triples.append((s, p, o))

			# add to indexed version
			if s not in graph.keys():
				graph[s] = {}
			if p not in graph[s].keys():
				graph[s][p] = {}
			graph[s][p][o] = True
			# print(graph)
			# input()

	print(len(nodes))
	print(len(predicates))
	print(len(triples))

	if types_file is not None:
		node_to_type, type_to_nodes = read_types_file(types_file)
		return nodes, predicates, triples, graph, node_to_type, type_to_nodes

	return nodes, predicates, triples, graph

def read_types_file(file_name):
	node_to_type = {}
	type_to_nodes = {}
	with open(file_name, 'r') as f:
		for line in f:
			node, p, node_type = line.strip().split('\t')
			node = int(node)

			if node not in node_to_type.keys():
				node_to_type[node] = []
			node_to_type[node].append(node_type)

			if node_type not in type_to_nodes.keys():
				type_to_nodes[node_type] = []
			type_to_nodes[node_type].append(node)

	return node_to_type, type_to_nodes


if __name__ == '__main__':
	# read_graph_txt('working_sample/complete_sample.txt')
	# read_graph_txt('data_files/robokop/robokop_singular_symm_rels.txt')
	read_graph_txt('robokop2_sample/sample_with_negs_wo_test_data2.txt')
	read_graph_txt('robokop2_sample/sample_duplicate_symm_rels.txt')
