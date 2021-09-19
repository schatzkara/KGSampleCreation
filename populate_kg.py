import sys
from constants import *
from read_graph_txt import read_graph_txt

def populate_kg(triple_file):
	nodes, predicates, triples, graph = read_graph_txt(triple_file)

	count = 0
	for node in nodes:
		n = list(GRAPH.run(f"CREATE (n)"))

	with open(subset_file, 'r') as f:
		skip = False
		for line in f:
			if skip:
				skip = False
				continue
			else:
				s, p, o = line.strip().split('\t')
				if p in GRAPH.symm_rels:
					skip = True

				rel = list(GRAPH.run("MATCH (e)-[r:{}]->(f) WHERE id(e)={} AND id(f)={} SET r.sample='{}' RETURN r".format(p, s, o, subset_name)))

				if len(rel) <= 0:
					print('failed on {} {} {}'.format(s, p, o))

				count += 1
				if count % 1000 == 0:
					print(count)

	print('{} edges were marked'.format(count))

	nodes = list(GRAPH.run("MATCH (e)-[r]->() WHERE r.sample='{} SET e.sample='{}' RETURN e".format(subset_name, subset_name)))

	print('{} nodes were marked'.format(len(nodes)))


if __name__ == '__main__':
	# mark_subset_in_neo4j('working_sample/complete_sample.txt', 'rw4mil', clear_previous=False)
	# mark_subset_in_neo4j('drkg_sample/drkg_complete_sample.txt', 'wo_test', clear_previous=False)
	# mark_drkg_subset_in_neo4j('drkg_treats_in_sample.txt', 'wo_test')

	# parse arguments
	script_name, predicate, start, split = sys.argv[0], sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

	mark_large_predicates_drkg(predicate, 'wo_test', start=start, split=split)
