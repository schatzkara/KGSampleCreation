import random
from constants import *
from file_reading.read_facts import read_facts
from read_graph_txt import read_graph_txt
from utils.graph_utils import clean_integer_output, get_entity_type


# txt version
def generate_negative_predicate(kg_file, types_file, predicate, n):
	# triples = list(GRAPH.run("MATCH (s)-[p:{}]-{}(o) RETURN id(s),type(p),id(o)".format(predicate, '>')))  # '' if predicate in GRAPH.symm_rels else '>'))
	nodes, predicates, triples, graph, node_to_type, type_to_nodes = read_graph_txt(kg_file, types_file)
	predicate_triples = [t for t in triples if t[1] == predicate]

	# print(triples)
	# input()
	negatives = []

	# randomly change s or o
	count = 0
	total = len(predicate_triples)
	for s, p, o in predicate_triples:
		# print(s, o)

		s_type = node_to_type[s]  # get_entity_type(s)
		possible_s_ids = []
		for t in s_type:
			possible_s_ids.extend(type_to_nodes[t])  # list(GRAPH.run("MATCH (s:{}) RETURN id(s)".format(':'.join(node_type))))
		# possible_ids = [x[0] for x in possible_ids]
		# possible_ids = [x for x in possible_ids if x in nodes]

		o_type = node_to_type[o]  # get_entity_type(o)
		possible_o_ids = []
		for t in o_type:
			possible_o_ids.extend(type_to_nodes[t])  # list(GRAPH.run("MATCH (o:{}) RETURN id(o)".format(':'.join(node_type))))
		# possible_ids = [x[0] for x in possible_ids]
		# possible_ids = [x for x in possible_ids if x in nodes]

		# generate n negatives for each positive
		for x in range(n):
			# change s
			if random.randint(0, 1) == 0:
				# print('changing s')
				if len(possible_s_ids) != 0:
					found = False
					while not found and len(possible_s_ids) != 0:
						rand_node = random.choice(possible_s_ids)  # [0]
						already_connected = in_kg(rand_node, p, o, triples)  # clean_integer_output(GRAPH.run("MATCH (s)-[p:{}]-(o) WHERE id(s)={} AND id(o)={} RETURN COUNT(*)".format(predicate, rand_node, o)))
						if not already_connected:
							negatives.append((rand_node, 'not_' + predicate, o))
							possible_s_ids.remove(rand_node)
							found = True
						else:
							possible_s_ids.remove(rand_node)

			# change o
			else:
				# print('changing o')
				if len(possible_o_ids) != 0:
					found = False
					while not found and len(possible_o_ids) != 0:
						rand_node = random.choice(possible_o_ids)  # [0]
						already_connected = in_kg(s, predicate, rand_node, triples)  # clean_integer_output(GRAPH.run("MATCH (s)-[p:{}]-(o) WHERE id(s)={} AND id(o)={} RETURN COUNT(*)".format(predicate, s, rand_node)))
						if not already_connected:
							negatives.append((s, 'not_' + predicate, rand_node))
							possible_o_ids.remove(rand_node)
							found = True
						else:
							possible_o_ids.remove(rand_node)

		# print(negatives[-1])
		count += 1
		if count % 50 == 0:
			print('{}/{}'.format(count, total))

	return negatives

def in_kg(s, p, o, triples):
	if p in GRAPH.symm_rels and (o, p, s) in triples:
		return True

	if (s, p, o) in triples:
		return True

	return False

# neo4j version
def generate_negative_predicate_neo4j(predicate, n):
	triples = list(GRAPH.run("MATCH (s)-[p:{}]-{}(o) RETURN id(s),type(p),id(o)".format(predicate, '>')))  # '' if predicate in GRAPH.symm_rels else '>'))

	# print(triples)
	# input()
	negatives = []

	# randomly change s or o
	count = 0
	total = len(triples)
	for s, p, o in triples:
		# print(s, o)
		# generate n negatives for each positive
		for x in range(n):
			# change s
			if random.randint(0, 1) == 0:
				# print('changing s')
				node_type = get_entity_type(s)
				possible_ids = list(GRAPH.run("MATCH (s:{}) RETURN id(s)".format(':'.join(node_type))))
				possible_ids = [x[0] for x in possible_ids]
				if len(possible_ids) != 0:
					found = False
					while not found and len(possible_ids) != 0:
						rand_node = random.choice(possible_ids)  # [0]
						already_connected = clean_integer_output(GRAPH.run("MATCH (s)-[p:{}]-(o) WHERE id(s)={} AND id(o)={} RETURN COUNT(*)".format(predicate, rand_node, o)))
						if not already_connected:
							negatives.append((rand_node, 'not_' + predicate, o))
							found = True
						else:
							possible_ids.remove(rand_node)

			# change o
			else:
				# print('changing o')
				node_type = get_entity_type(o)
				possible_ids = list(GRAPH.run("MATCH (o:{}) RETURN id(o)".format(':'.join(node_type))))
				possible_ids = [x[0] for x in possible_ids]
				if len(possible_ids) != 0:
					found = False
					while not found and len(possible_ids) != 0:
						rand_node = random.choice(possible_ids)  # [0]
						already_connected = clean_integer_output(GRAPH.run("MATCH (s)-[p:{}]-(o) WHERE id(s)={} AND id(o)={} RETURN COUNT(*)".format(predicate, s, rand_node)))
						if not already_connected:
							negatives.append((s, 'not_' + predicate, rand_node))
							found = True
						else:
							possible_ids.remove(rand_node)

		# print(negatives[-1])
		count += 1
		if count % 10 == 0:
			print('{}/{}'.format(count, total))

	return negatives

def add_negative_predicates_to_neo4j(file_name, sample):
	negatives = read_facts(file_name)
	query = "MATCH (s), (o) WHERE id(s)={} AND id(o)={} CREATE (s)-[r:{}]->(o) SET r.sample='{}' RETURN r".format(sample)

	for s, p, o in negatives:
		result = list(GRAPH.run(query.format(s, o, p)))
		if len(result) < 1:
			print('failed on {} {} {}'.format(s, p, o))


if __name__ == '__main__':
	# kg_file = 'sample2.txt'
	# types_file = 'robokop_singular_symm_rels_types.txt'
	# negatives = generate_negative_predicate(kg_file, types_file, 'treats', 1)
	# print(negatives)

	# file_name = 'generated_negatives.txt'
	# with open(file_name, 'w') as f:
	# 	for s, p, o in negatives:
	# 		f.write('{}\t{}\t{}\n'.format(s, p, o))

	# add_negative_predicates_to_neo4j('working_sample/generated_negatives.txt')

	kg_file = 'drkg.txt'
	types_file = 'drkg_types.txt'
	negatives = generate_negative_predicate(kg_file, types_file, 'treats', 1)

	file_name = 'generated_negatives_drkg.txt'
	with open(file_name, 'w') as f:
		for s, p, o in negatives:
			f.write('{}\t{}\t{}\n'.format(s, p, o))

	# add_negative_predicates_to_neo4j('generated_negatives_drkg.txt')
