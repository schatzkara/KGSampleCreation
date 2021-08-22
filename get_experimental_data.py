import os
import random
from constants import *
from read_graph_txt import read_graph_txt
from utils.graph_utils import clean_integer_output, get_entity_type


def get_hypothesized_facts_txt(kg_file, output_file, n, predicate):
	with open(kg_file, 'r') as f:
		triples = f.readlines()

	triples = [t.strip().split('\t') for t in triples]
	predicate_triples = [t for t in triples if t[1] == predicate]
	# print(triples[:3])

	hypothesized_facts = []
	for x in range(n):
		fact = random.choice(predicate_triples)
		predicate_triples.remove(fact)
		triples.remove(fact)
		hypothesized_facts.append(fact)

	head, tail = os.path.split(kg_file)
	name, ext = tail.split('.')
	output_file2 = os.path.join(head, name + '_wo_test_data.' + ext)
	# print(output_file)

	with open(output_file2, 'w') as f:
		for s, p, o in triples:
			f.write('{}\t{}\t{}\n'.format(s, p, o))

	with open(output_file, 'w') as f:
		for s, p, o in hypothesized_facts:
			f.write('{}\t{}\t{}\n'.format(s, p, o))

def get_negative_examples(kg_file, types_file, pos_file, output_file, n):
	nodes, predicates, triples, graph, node_to_type, type_to_nodes = read_graph_txt(kg_file, types_file)

	negatives = {}
	with open(pos_file, 'r') as f:
		for line in f:
			s, p, o = line.strip().split('\t')
			s, o = int(s), int(o)
			negatives[line] = []

			s_type = node_to_type[s]
			possible_s_ids = []
			for t in s_type:
				possible_s_ids.extend(type_to_nodes[t]) 

			o_type = node_to_type[o]
			possible_o_ids = []
			for t in o_type:
				possible_o_ids.extend(type_to_nodes[t])   

			for x in range(n):
				if random.randint(0, 1) == 0:
					# change subject
					if len(possible_s_ids) != 0:
						found = False
						while not found and len(possible_s_ids) != 0:
							rand_node = random.choice(possible_s_ids)
							already_connected = in_kg(rand_node, p, o, triples)
							if not already_connected:
								negatives[line].append((rand_node, p, o))
								possible_s_ids.remove(rand_node)
								found = True
							else:
								possible_s_ids.remove(rand_node)

				else:
					# change object
					if len(possible_o_ids) != 0:
						found = False
						while not found and len(possible_o_ids) != 0:
							rand_node = random.choice(possible_o_ids)
							already_connected = in_kg(s, p, rand_node, triples)
							if not already_connected:
								negatives[line].append((s, p, rand_node))
								possible_o_ids.remove(rand_node)
								found = True
							else:
								possible_o_ids.remove(rand_node)

	with open(output_file, 'w') as f:
		for pos, negs in negatives.items():
			negs = ['{}\t{}\t{}'.format(s, p, o) for s, p, o in negs]
			f.write('{}\t\t{}\n'.format(pos.strip(), '\t\t'.join(negs)))

def get_other_hypothesized_facts(kg_file, types_file, output_file, n, predicate):
	nodes, predicates, triples, graph, node_to_type, type_to_nodes = read_graph_txt(kg_file, types_file)

	predicate_triples = [t for t in triples if t[1] == predicate]

	possible_triples = list(GRAPH.run(f"MATCH (e0)-[:{predicate}]-{'>' if predicate not in GRAPH.symm_rels else ''}(e1) RETURN id(e0),id(e1)"))
	hypothesized_facts = []
	for e0, e1 in possible_triples:
		if e0 in nodes and e1 in nodes:
			# print('entities there')
			if not in_kg(e0, predicate, e1, triples):
				# print('triple not there')
				# print((int(e0), predicate, int(e1)))
				hypothesized_facts.append((e0, predicate, e1))

	random.shuffle(hypothesized_facts)

	with open(output_file, 'w') as f:
		for s, p, o in hypothesized_facts:
			f.write('{}\t{}\t{}\n'.format(s, p, o))


def in_kg(s, p, o, triples):
	if p in GRAPH.symm_rels and (o, p, s) in triples:
		return True

	if (s, p, o) in triples:
		return True

	return False

# def get_hypothesized_facts_neo4j(output_file, n):
# 	facts = {}
# 	min_id = clean_integer_output(GRAPH.run("MATCH ()-[p]-() RETURN MIN(id(p))"), label="MIN(id(p))")
# 	max_id = clean_integer_output(GRAPH.run("MATCH ()-[p]-() RETURN MAX(id(p))"), label="MAX(id(p))")
# 	for i in range(n):
# 		found = False
# 		while not found:
# 			rand_id = random.randint(min_id, max_id)
# 			if rand_id not in facts.keys():
# 				triple = list(GRAPH.run("MATCH (s)-[p]->(o) WHERE id(p)={} RETURN id(s), type(p), id(o)".format(rand_id)))
# 				if len(triple) != 0:
# 					s = triple[0][0]  # ["id(s)"]
# 					p = triple[0][1]
# 					o = triple[0][2]  # ["id(o)"]
# 					facts[rand_id] = (s, p, o)
# 					found = True

# 	with open(output_file, 'w') as f:
# 		for triple_id, (s, p, o) in facts.items():
# 			f.write('{}\t{}\t{}\t{}\n'.format(triple_id, s, p, o))

# def get_hypothesized_facts_neo4j(output_file, n, predicate):
# 	facts = {}
# 	ids = list(GRAPH.run("MATCH ()-[p:{}]-{}() RETURN DISTINCT id(p))".format(predicate, '' if predicate in GRAPH.symm_rels else '>')))
# 	for i in range(n):
# 		found = False
# 		while not found:
# 			rand_id = random.choice(ids)
# 			if rand_id not in facts.keys():
# 				triple = list(GRAPH.run("MATCH (s)-[p]->(o) WHERE id(p)={} RETURN id(s), type(p), id(o)".format(rand_id)))
# 				if len(triple) != 0:
# 					s = triple[0][0]  # ["id(s)"]
# 					p = triple[0][1]
# 					o = triple[0][2]  # ["id(o)"]
# 					facts[rand_id] = (s, p, o)
# 					found = True

# 	with open(output_file, 'w') as f:
# 		for triple_id, (s, p, o) in facts.items():
# 			f.write('{}\t{}\t{}\t{}\n'.format(triple_id, s, p, o))

# def get_negative_examples(pos_facts_file, n):
# 	neg_facts = {}
# 	with open(pos_facts_file, 'r') as f:
# 		for line in f:
# 			triple_id, s, p, o = line.strip().split('\t')
# 			neg_facts[triple_id] = []
# 			node_type = get_entity_type(o)
# 			print('here1')
# 			possible_ids = list(GRAPH.run("MATCH (s)-[p:{}]-(),(o:{}) WHERE id(s)={} AND NOT EXISTS((s)-[p]-(o)) RETURN id(o)".format(p, ':'.join(node_type), s)))
# 			print('here2')
# 			if len(possible_ids) != 0:
# 				print(possible_ids)
# 				random_nodes = []
# 				for i in range(n):
# 					found = False
# 					while not found:
# 						rand_node = random.choice(possible_ids)
# 						if rand_node not in random_nodes: 
# 							random_nodes.append(rand_node)
# 							neg_facts[triple_id].append((s, p, rand_node))
# 							found = True
# 			else:
# 				print('there were no nodes to choose from for triple_id:{}...'.format(triple_id))

# def get_negative_examples(pos_facts_file, output_file, n):
# 	neg_facts = {}
# 	with open(pos_facts_file, 'r') as f:
# 		for line in f:
# 			triple_id, s, p, o = line.strip().split('\t')
# 			neg_facts[triple_id] = []

# 			node_type = get_entity_type(o)
# 			possible_ids = list(GRAPH.run("MATCH (o:{}) RETURN id(o)".format(':'.join(node_type))))
# 			if len(possible_ids) != 0:
# 				random_nodes = []
# 				for i in range(n):
# 					found = False
# 					while not found:
# 						rand_node = random.choice(possible_ids)
# 						if rand_node not in random_nodes: 
# 							already_connected = clean_integer_output(GRAPH.run("MATCH (s)-[p:{}]-(o) WHERE id(s)={} AND id(o)={} RETURN COUNT(*)".format(p, s, rand_node)))
# 							if not already_connected:
# 								random_nodes.append(rand_node)
# 								neg_facts[triple_id].append((s, p, rand_node))
# 								found = True
# 							else:
# 								possible_ids.remove(rand_node)
# 			else:
# 				print('there were no nodes to choose from for triple_id:{}...'.format(triple_id))

# 			node_type = get_entity_type(s)
# 			possible_ids = list(GRAPH.run("MATCH (s:{}) RETURN id(s)".format(':'.join(node_type))))
# 			if len(possible_ids) != 0:
# 				random_nodes = []
# 				for i in range(n):
# 					found = False
# 					while not found:
# 						rand_node = random.choice(possible_ids)
# 						if rand_node not in random_nodes: 
# 							already_connected = clean_integer_output(GRAPH.run("MATCH (s)-[p:{}]-(o) WHERE id(s)={} AND id(o)={} RETURN COUNT(*)".format(p, rand_node, o)))
# 							if not already_connected:
# 								random_nodes.append(rand_node)
# 								neg_facts[triple_id].append((rand_node, p, o))
# 								found = True
# 							else:
# 								possible_ids.remove(rand_node)
# 			else:
# 				print('there were no nodes to choose from for triple_id:{}...'.format(triple_id))

# 	with open(output_file, 'w') as f:
# 		for triple_id, negs in neg_facts.items():
# 			for (s, p, o) in negs:
# 				f.write('{}\t{}\t{}\t{}\n'.format(triple_id, s, p, o))


if __name__ == '__main__':
	# pos_file = 'working_sample/hypothesized_facts.txt'
	# neg_file = 'hypothesized_negatives2.txt'

	# get_hypothesized_facts(pos_file, 5)
	# get_negative_examples_2(pos_file, neg_file, 2)
	# get_hypothesized_facts_txt('working_sample/sample2_with_negs.txt', pos_file, 50, 'treats')
	# get_negative_examples('working_sample/sample2_with_negs.txt', 'robokop_types.txt', pos_file, neg_file, 5)

	# get_other_hypothesized_facts('working_sample/sample2_with_negs.txt', 'data_files/robokop/robokop_types.txt', 'other_hypothesized_facts.txt', 50, 'treats')
	# get_negative_examples('working_sample/sample2_with_negs.txt', 'data_files/robokop/robokop_types.txt', 'other_hypothesized_facts.txt', 'other_hypothesized_negatives.txt', 5)

	# nodes, predicates, triples, graph, node_to_type, type_to_nodes = read_graph_txt('working_sample/sample2_with_negs.txt', 'data_files/robokop/robokop_types.txt')
	# print(in_kg(412707, 'treats', 11361, triples))
	# print(type(triples[0][0]))
	# print(triples[0])

	kg_file = 'drkg_with_negs.txt'
	types_file = 'drkg_types.txt'
	pos_file = 'hypothesized_facts.txt'
	neg_file = 'hypothesized_negatives.txt'

	# get_hypothesized_facts_txt(kg_file, pos_file, 250, 'treats')
	# get_negative_examples(kg_file, types_file, pos_file, neg_file, 5)

	get_hypothesized_facts_txt('drkg_with_negs_wo_test_data.txt', 'other_hypothesized_facts.txt', 100, 'treats')
