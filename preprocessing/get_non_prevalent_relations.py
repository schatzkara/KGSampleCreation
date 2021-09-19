from constants import *

def get_non_prevalent_relations(graph, cutoff_percentile, output_file):
	size = graph.size()
	cutoff = size * cutoff_percentile

	non_prevalent_rels = []

	result = list(graph.run("MATCH ()-[r]->() RETURN type(r), count(*) ORDER BY count(*)"))
	for r in result:
		rel, count = r
		if count < cutoff:
			non_prevalent_rels.append(rel)

	with open(output_file, 'w') as f:
		for rel in non_prevalent_rels:
			f.write('{}\n'.format(rel))

	return non_prevalent_rels


if __name__ == '__main__':
	get_non_prevalent_relations(GRAPH, 0.01, 'non_prevalent_rels_1.txt')