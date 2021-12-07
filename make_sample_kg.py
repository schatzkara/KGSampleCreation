from os.path import exists
from constants import *
from file_reading.read_graph_txt import read_graph_txt

def get_entity_labels_and_names(input_file, output_file):
	nodes, predicates, triples, graph = read_graph_txt(input_file)

	if exists(output_file):
		with open(output_file, 'r') as f:
			done_nodes = set([int(line.strip().split('\t')[0]) for line in f.readlines()])
	else:
		done_nodes = []

	count = 0
	total = len(nodes)
	for n in nodes:
		if n not in done_nodes:
			labels, name = list(GRAPH.run(f"MATCH (e) WHERE id(e)={n} RETURN labels(e),e.name"))[0]
			
			try:
				with open(output_file, 'a', encoding='utf-8') as f:
					f.write(f"{n}\t{','.join(labels)}\t{name}\n")
			except:
				print(type(labels), labels)
				print(type(name), name)
				quit()

		count += 1
		if count % 1000 == 0:
			print(f"{count}/{total}")

def create_kg(input_file, node_file, id_mapping_file):
	with open(id_mapping_file, 'r', encoding='utf-8') as f:
		done_nodes = set([line.strip().split('\t')[0] for line in f.readlines()])

	count = 0
	with open(node_file, 'r', encoding='utf-8') as f:
		for line in f:
			node, labels, name = line.strip().split('\t')

			if node not in done_nodes:
				labels = labels.split(',')

				create_node = f'CREATE (n:`{"`:`".join(labels)}` {{ id: {node}, name: "`{name}`" }}) RETURN id(n)'
				# print(create_node)
				# input()
				node_id = list(GRAPH.run(create_node))[0][0]
				# print(node)

				with open(id_mapping_file, 'a', encoding='utf-8') as f:
					f.write(f"{node}\t{node_id}\n")

			count += 1
			if count % 1000 == 0:
				print(count)

	with open('created_edges.txt', 'r') as f:
		done_edges = set(f.readlines())

	count = 0
	with open(input_file, 'r') as f:
		for line in f:
			if line not in done_edges:
				# print(line)
				s, p, o = line.strip().split('\t')

				create_edge = f"MATCH (e:`biolink:NamedThing`),(f:`biolink:NamedThing`) WHERE e.id={s} AND f.id={o} CREATE (e)-[r:`{p}`]->(f)"
				# print(create_edge)
				GRAPH.run(create_edge)

				with open('created_edges.txt', 'a') as f:
					f.write(line)
				# print(line)

			count += 1
			if count % 1000 == 0:
				print(count)


if __name__ == '__main__':
	input_file = 'robokop2-2_sample/sample_with_negs.txt'
	output_file = 'robokop2-2_sample/node_labels_and_names.txt'
	get_entity_labels_and_names(input_file, output_file)

	input_file = 'robokop2-2_sample/sample_with_negs_wo_test_data2.txt'
	node_file = 'robokop2-2_sample/node_labels_and_names.txt'
	id_mapping_file = 'robokop2-2_sample/robokop2-2_to_rk2-2sample_id_mappings.txt'
	create_kg(input_file, node_file, id_mapping_file)

	# read_graph_txt(input_file)
