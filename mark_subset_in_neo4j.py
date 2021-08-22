from constants import *

def mark_subset_in_neo4j(subset_file, subset_name, clear_previous):
	if clear_previous:
		clear_previous_subset()

	count = 0
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

def clear_previous_subset():
	# result = list(GRAPH.run("MATCH ()-[r]->() SET r.sample=null"))
	result = list(GRAPH.run("MATCH ()-[r]->() DELETE r.sample"))

	print('edges were unmarked')


if __name__ == '__main__':
	mark_subset_in_neo4j('working_sample/complete_sample.txt', 'rw4mil', clear_previous=False)
