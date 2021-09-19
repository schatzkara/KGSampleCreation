import os
from constants import *
from utils.graph_utils import extract_deepest_labels, get_entity_type


def kg_to_txt(output_file, duplicate_symm_rels=True):
	# query = "MATCH (e)-[r]->(f) RETURN DISTINCT id(e),type(r),id(f)"
	# triples = list(GRAPH.run(query))
	rel_query = 'MATCH ()-[r]-() RETURN DISTINCT type(r)'
	rels = list(GRAPH.run(rel_query))
	rels = sorted([r[0] for r in rels])
	print(len(rels))

	triples = {}

	for r in rels:
		print(r)
		endpoint_query = 'MATCH (a)-[r:`{}`]-{}(b) RETURN DISTINCT id(a),id(b)'.format(r, '' if duplicate_symm_rels and r in GRAPH.symm_rels else '>')
		endpoints = list(GRAPH.run(endpoint_query))
		triples[r] = endpoints

	with open(output_file, 'w') as f:
		for r, endpoints in triples.items():
			for a, b in endpoints:
				f.write('{}\t{}\t{}\n'.format(a, r, b))

def duplicate_symm_rels(file_name, output_file):
	# output_file = 'updated_' + file_name
	with open(output_file, 'w') as f:
		with open(file_name, 'r') as g:
			for line in g:
				f.write(line)

				s, p, o = line.strip().split('\t')
				if p in GRAPH.symm_rels:
					f.write('{}\t{}\t{}\n'.format(o, p, s))
					

if __name__ == '__main__':
	# kg_to_txt('rk.txt', duplicate_symm_rels=False)
	# add_node_types('../db_dumps/robokop_node_types.txt')
	# node_types_to_triple('../db_dumps/robokop_node_types.txt')
	# duplicate_symm_rels('working_sample/sample2_with_negs_wo_test_data.txt', 'working_sample/complete_sample.txt')
	# make_types_file('robokop_singular_symm_rels.txt')
	# duplicate_symm_rels('../rk_sample.txt', '../complete_sample.txt')

	kg_to_txt('drkg.txt', duplicate_symm_rels=False)
	make_types_file('drkg.txt')
	duplicate_symm_rels('drkg_with_negs_wo_test_data_wo_test_data.txt', 'complete_sample.txt')
