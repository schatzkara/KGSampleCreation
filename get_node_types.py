import os
from utils.graph_utils import extract_deepest_labels, get_entity_type


def make_types_file(file_name):
	head, tail = os.path.split(file_name)
	name, ext = tail.split('.')
	output_file = os.path.join(head, name + '_types.' + ext)

	print(output_file)

	nodes = set()
	node_types = {}
	with open(file_name, 'r') as f:
		f = f.readlines()
		count = 0
		total = len(f)
		for line in f:
			a, r, b = line.strip().split('\t')
			if a not in nodes:
				t = get_entity_type(a)
				for i in t:
					if i not in node_types.keys():
						node_types[i] = set()
					node_types[i].add(a)
				nodes.add(a)
			if b not in nodes:
				t = get_entity_type(b)
				for i in t:
					if i not in node_types.keys():
						node_types[i] = set()
					node_types[i].add(b)
				nodes.add(b)

			count += 1
			if count % 10000 == 0:
				print('{}/{}'.format(count, total))

	node_types = sorted(node_types.items(), key=lambda x: (x[0], x[1]))

	with open(output_file, 'w') as g:
		for t, nodes in node_types:
			for n in nodes:
				g.write('{}\ttype_of\t{}\n'.format(n, t))				


if __name__ == '__main__':
	# kg_to_txt('rk.txt', duplicate_symm_rels=False)
	# add_node_types('../db_dumps/robokop_node_types.txt')
	# node_types_to_triple('../db_dumps/robokop_node_types.txt')
	# duplicate_symm_rels('working_sample/sample2_with_negs_wo_test_data.txt', 'working_sample/complete_sample.txt')
	# make_types_file('robokop_singular_symm_rels.txt')
	# duplicate_symm_rels('../rk_sample.txt', '../complete_sample.txt')

	# kg_to_txt('drkg.txt', duplicate_symm_rels=False)
	make_types_file('drkg.txt')
