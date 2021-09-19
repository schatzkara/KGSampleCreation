def node_types_to_triple(output_file):
	types = {}
	type_query = 'MATCH (e:Concept) RETURN DISTINCT id(e),e.name'
	result = list(GRAPH.run(type_query))
	for ID,name in result:
		types[name] = ID

	for t in types.keys():
		print(t)
		query = "MATCH (e:{}) RETURN DISTINCT id(e)".format(t)
		# print(query)
		result = list(GRAPH.run(query))
		count = 0
		total = len(result)
		for node in result:
			# print(node)
			# input()
			with open(output_file, 'a') as f:
				f.write('{}\ttype_of\t{}\n'.format(node, t))

			count += 1
			if count % 100000 == 0:
				print('{}/{}'.format(count, total))


def add_node_types(file_name):
	head, tail = os.path.split(file_name)
	name, ext = tail.split('.')
	output_file = os.path.join(head, name + '_with_types.' + ext)

	types = {}
	type_query = 'MATCH (e:Concept) RETURN DISTINCT id(e),e.name'
	result = list(GRAPH.run(type_query))
	for ID,name in result:
		types[name] = ID

	nodes = set()
	node_types = {}
	query = "MATCH (e) WHERE id(e)={} RETURN labels(e)"
	with open(file_name, 'r') as f:
		f = f.readlines()
		count = 0
		total = len(f)
		for line in f:
			a, r, b = line.strip().split('\t')
			if a not in nodes:
				result = GRAPH.run(query.format(a))
				result = list(list(result)[0])[0]
				t = extract_deepest_labels(result)
				for i in t:
					if i not in node_types.keys():
						node_types[i] = set()
					node_types[i].add(a)
			if b not in nodes:
				result = GRAPH.run(query.format(b))
				result = list(list(result)[0])[0]
				t = extract_deepest_labels(result)
				for i in t:
					if i not in node_types.keys():
						node_types[i] = set()
					node_types[i].add(b)

			with open(output_file, 'a') as g:
				g.write(line)

			count += 1
			if count % 1000 == 0:
				print('{}/{}'.format(count, total))

	with open(output_file, 'a') as g:
		for t, nodes in node_types.items():
			if t in types.keys():
				t = types[t]
				for n in nodes:
					g.write('{}\ttype_of\t{}\n'.format(n, t))			
