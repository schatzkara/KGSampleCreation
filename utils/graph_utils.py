from constants import *

# def get_graph_size(graph):
# 	"""Gets the size of the given graph, i.e. the number of edges.
# 	:param graph: (py2neo.Graph) the graph to get the size of
# 	:returns: (int) the size of the graph
# 	"""
# 	size_query = 'MATCH ()-[r]-() RETURN COUNT(*)'
# 	graph_size = list(graph.run(size_query))  # 14,695,902 ... 32,442,448
# 	graph_size = int(graph_size[0]['COUNT(*)'])

# 	return graph_size

def get_edge_weight(edge):
	# TODO #
	s, o = get_node_curie(edge.s), get_node_curie(edge.o)

	all_pubs = 27840000
	sub_pubs = get_num_pubs(s) 
	obj_pubs = get_num_pubs(o)
	both_pubs = get_num_pubs(s, o)

	# if edge['type'] == 'literature_co-occurrence':

	cov = (both_pubs / all_pubs) - (sub_pubs / all_pubs) * (obj_pubs / all_pubs)

def get_node_degree(node_id, direction=None, predicate=None, sample=None):
	# part1 = "MATCH (e) WHERE id(e)={}".format(node_id)
	# part2 = "RETURN apoc.node.degree(e{})"
	# if predicate is None:
	# 	if direction is None:
	# 		part2 = part2.format("")
	# 	else:
	# 		part2 = part2.format(", '>'" if direction == FROM else ", '<'")
	# else:
	# 	if direction is None:
	# 		part2 = part2.format(", '{}'".format(predicate))
	# 	else:
	# 		part2 = part2.format(", '{}>'" if direction == FROM else ", '<{}'")
	# 		part2 = part2.format(predicate)
	# query = part1 + " " + part2
	match_clause = "MATCH ({})-[r{}]-{}({})"
	if predicate is None:
		if direction is None:
			match_clause = match_clause.format('e', '', '', '')
		else:
			if direction == FROM:
				match_clause = match_clause.format('e', '', '>', '')
			elif direction == TO:
				match_clause = match_clause.format('', '', '>', 'e')
			else:
				print(direction, 'not allowed')
	else:
		if direction is None:
			match_clause = match_clause.format('e', ':{}'.format(predicate), '', '')
		else:
			if direction == FROM:
				match_clause = match_clause.format('e', ':{}'.format(predicate), '>', '')
			elif direction == TO:
				match_clause = match_clause.format('', ':{}'.format(predicate), '>', 'e')
			else:
				print(direction, 'not allowed')
	where_clause = "WHERE id(e)={}".format(node_id)
	if sample is not None:
		where_clause += " AND r.sample='{}'".format(sample)
	return_clause = "RETURN DISTINCT COUNT(*)"
	query = match_clause + " " + where_clause + " " + return_clause
	# print(query)

	return clean_integer_output(GRAPH.run(query))

def clean_integer_output(output, label="COUNT(*)"):
	return 0 if output is None else list(list(output)[0])[0]  # int(list(output)[0])  # int(list(output)[0][label])

def get_entity_name(entity_id):
	query = "MATCH (e) WHERE id(e)={} RETURN e.name".format(entity_id)
	name = str(list(GRAPH.run(query))[0])

	return name

def extract_full_labels(label):
	labels = []
	parent = label
	while parent is not None:
		labels.append(parent)
		parent = GRAPH.entity_type_parents[parent]

	return labels

def extract_deepest_labels(labels):
	"""Determines the deepest/most specific labels from the given list of labels, according to the type hierarchy.
	:param labels: (list) the list of labels
	:returns: (list) list of deepest/most specific labels from labels
	"""
	if labels == ['Concept']:
		return labels
	
	result = []
	deepest = 0
	for l in labels:
		if l == 'macromolecular_machine':
			l = 'macromolecular_machine_mixin'
		depth = get_label_depth(l)
		if depth > deepest:
			result = [l]
			deepest = depth
		elif depth == deepest:
			result.append(l)

	if 'macromolecular_machine_mixin' in result:
		result.remove('macromolecular_machine_mixin')
		result.append('macromolecular_machine')

	return result

def get_label_depth(label):
	"""Computes the depth of the given label according to the type hierarchy.
	:param label: (str) the label whose depth is desired
	:returns: (int) the depth of label
	"""
	parent = GRAPH.entity_type_parents[label]
	depth = 0
	while parent is not None:
		parent = GRAPH.entity_type_parents[parent]
		depth += 1

	return depth

def subtype_of(sub, sup):
	"""Determines if the the given label lists have a subtype relationship according to the type hierarchy.
	Note that the given labels are lists of labels, rather than single labels.
	:param sub: (list) the proposed subtype
	:param sup: (list) the proposed supertype
	:returns: (boolean) true if sub is a subtype of sup or they are the same, false otherwise
	"""
	if sub == sup:
		return True
	# if len(sub) == 1 and len(sup) == 1:

	for s in sub:
		for t in sup:
			if subtype_of_helper(s, t):
				return True
	
	return False

def subtype_of_helper(sub, sup):
	"""Determines if the given labels have a subtype relationship according to the type hierarchy.
	Note that the given labels are single labels.
	:param sub: (str) the proposed subtype
	:param sup: (str) the proposed supertype
	:returns: (boolean) true if sub is a subtype of sup or they are the same, false otherwise
	"""
	# if sub == sup:
	# 	return True
	# # if sub == 'Concept' or sup == 'Concept':
	# # 	return False
	# parent = GRAPH.entity_type_parents[sub]
	# while parent is not None:
	# 	if parent == sup:
	# 		return True
	# 	parent = GRAPH.entity_type_parents[parent]

	# return False	
	return sub == sup or descendant_of(sub, sup)

def descendant_of(d, a):
	parent = GRAPH.entity_type_parents[d]
	while parent is not None:
		if parent == a:
			return True
		parent = GRAPH.entity_type_parents[parent]

	return False

def supertype_of(sup, sub):
	"""Determines if the the given label lists have a supertype relationship according to the type hierarchy.
	Note that the given labels are lists of labels, rather than single labels.
	:param sup: (list) the proposed supertype
	:param sub: (list) the proposed subtype
	:returns: (boolean) true if sup is a supertype of sub or they are the same, false otherwise
	"""
	if sup == sub:
		return True

	for s in sup:
		for t in sub:
			if supertype_of_helper(s, t):
				return True

	return False

def supertype_of_helper(sup, sub):
	"""Determines if the given labels have a supertype relationship according to the type hierarchy.
	Note that the given labels are single labels.
	:param sup: (str) the proposed supertype
	:param sub: (str) the proposed subtype
	:returns: (boolean) true if sup is a supertype of sub or they are the same, false otherwise
	"""
	# if sup == sub:
	# 	return True
	# # if sup == 'Concept' or sub == 'Concept':
	# # 	return False
	# parent = GRAPH.entity_type_parents[sub]
	# while parent is not None:
	# 	if parent == sup:
	# 		return True
	# 	parent = GRAPH.entity_type_parents[parent]

	# return False
	return sup == sub or ancestor_of(sup, sub)

def ancestor_of(a, d):
	parent = GRAPH.entity_type_parents[d]
	while parent is not None:
		if parent == a:
			return True
		parent = GRAPH.entity_type_parents[parent]

	return False

def entity_subpath_of(sub, sup):
	return sub == sup or proper_entity_subpath_of(sub, sup)

def proper_entity_subpath_of(sub, sup):
	if len(sub) != len(sup):
		return False

	if sub == sup:
		return False

	for i in range(len(sub)):
		if not subtype_of(sub[i], sup[i]):
			return False

	return True

def entity_superpath_of(sup, sub):
	return sup == sub or proper_entity_superpath_of(sup, sub)

def proper_entity_superpath_of(sup, sub):
	if len(sup) != len(sub):
		return False

	if sup == sub:
		return False

	for i in range(len(sup)):
		if not supertype_of(sup[i], sub[i]):
			return False

	return True

def get_entity_id(e):
	"""Gets the entity id for the entity with the given name.
	:param e: (str) the name of the entity
	:returns: (int) the entity id
	"""
	query = "MATCH (e) WHERE e.name='{}' RETURN id(e)".format(e)
	result = int(str(list(GRAPH.run(query))[0]))

	return result

def get_entity_type(eid):
	"""Gets the entity labels for the entity with the given id.
	:param eid: (int) the entity id
	:returns: (list) the entity labels
	"""
	query = "MATCH (e) WHERE id(e)={} RETURN labels(e)".format(eid)
	result = list(GRAPH.run(query))[0][0]
	etype = extract_deepest_labels(result)

	return etype

def triple_in_KG(s, p, o):
	"""Determines if the given triple exists in the knowledge graph.
	:param s: (str) the name of the subject of the triple
	:param p: (str) the relationship type of the triple
	:param o: (str) the name of the object of the triple
	:returns: (boolean) True if the triple exists in the knowledge graph, False otherwise
	"""
	query = "MATCH (s)-[p:`{}`]-(o) WHERE id(s)={} AND id(o)={} RETURN s,p,o".format(p, s, o)
	result = list(GRAPH.run(query))

	return True if len(result) > 0 else False


if __name__ == '__main__':
	# print(supertype_of(['Concept'], ['Concept']))
	# print(supertype_of(['Concept'], ['disease']))
	# print(supertype_of(['gene'], ['Concept']))
	# labels = ['disease', 'biological_entity', 'named_thing', 'cell', 'anatomical_entity']
	# for l in labels:
	# 	print(l)
	# 	print(extract_full_labels(l))
	print(get_node_degree(11546, None, 'treats'))
