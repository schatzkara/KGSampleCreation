import yaml
from py2neo import Graph

input_file = 'C://Users//Kara//Documents//Research//ExternalSourceCode//biolink-model//biolink-model.yaml'
output_file = 'type_hierarchy.txt'

def get_entity_type_hierarchy(input_file, output_file):
	"""Extracts the type hierarchy from the biolink yaml file.
	:param input_file: (str) the biolink yaml file, where the hierarchy is stored
	:param output_file: (str) the file where the extracted hierarchy should be written
	"""
	# the connection to neo4j
	HOST = 'localhost'
	PORT = 7687
	USER = 'neo4j'
	PASS = 'password'
	GRAPH = Graph(host=HOST, port=PORT, user=USER, password=PASS)
	
	query = 'MATCH (e0) RETURN DISTINCT labels(e0)'
	result = list(GRAPH.run(query))
	all_labels = set()
	for r in result:
		all_labels.update(list(r)[0])
	# all_labels.add('macromolecular_machine_mixin')

	all_labels = [convert_rk_entity_type_to_biolink(l) for l in all_labels]

	parents = {}
	children = {}

	with open(input_file, encoding='utf=8') as f:
		model = yaml.full_load(f)

		classes = model['classes']

		for key in classes.keys():
			items = classes[key]

			# key = key.replace(' ', '_')

			if key not in all_labels:
				continue

			if 'is_a' not in items.keys():
				parents[key] = None
				children[key] = []
			else:
				parent = items['is_a']  # .replace(' ', '_')
				if key not in parents.keys():
					parents[key] = None
				if key not in children.keys():
					children[key] = []

				if parent not in parents.keys() and parent in all_labels:
					parents[parent] = None
				if parent not in children.keys() and parent in all_labels:
					children[parent] = []
				
				if parent in all_labels:
					parents[key] = parent
					children[parent].append(key)

	with open(output_file, 'w') as f:
		if parents.keys() != children.keys():
			print('ERROR')
		for node_type in parents.keys():
			p = convert_biolink_entity_type_to_rk(parents[node_type])
			c = [convert_biolink_entity_type_to_rk(child) for child in children[node_type]]
			node_type = convert_biolink_entity_type_to_rk(node_type)
			f.write('{}\t{}\t{}\n'.format(node_type, p, ",".join(c)))

def convert_rk_entity_type_to_biolink(name):
	name = name.split(':')[1]
	result = ''
	for letter in name:
		if letter.isupper():
			result += ' '
		result += letter
	result = result[1:].lower()

	return result

def convert_biolink_entity_type_to_rk(name):
	print(name)
	if name is None:
		return None

	result = 'biolink:'
	uppercase_next = True
	for letter in name:
		if uppercase_next:
			result += letter.upper()
			uppercase_next = False
		elif letter == ' ':
			uppercase_next = True
		else: 
			result += letter

	print(result)

	return result

def get_predicate_hierarchy(input_file, output_file):
	"""Extracts the type hierarchy from the biolink yaml file.
	:param input_file: (str) the biolink yaml file, where the hierarchy is stored
	:param output_file: (str) the file where the extracted hierarchy should be written
	"""
	# the connection to neo4j
	HOST = 'localhost'
	PORT = 7687
	USER = 'neo4j'
	PASS = 'password'
	GRAPH = Graph(host=HOST, port=PORT, user=USER, password=PASS)
	
	query = 'MATCH ()-[r]->() RETURN DISTINCT type(r)'
	result = list(GRAPH.run(query))
	all_types = set()
	for r in result:
		all_types.add(r[0])

	all_types = [convert_rk_predicate_to_biolink(l) for l in all_types]

	parents = {}
	children = {}

	with open(input_file, encoding='utf=8') as f:
		model = yaml.full_load(f)

		slots = model['slots']

		for key in slots.keys():
			items = slots[key]

			# key = key.replace(' ', '_')

			if key not in all_types:
				continue

			if 'is_a' not in items.keys():
				parents[key] = None
				children[key] = []
			else:
				parent = items['is_a']  # .replace(' ', '_')
				if key not in parents.keys():
					parents[key] = None
				if key not in children.keys():
					children[key] = []

				if parent not in parents.keys() and parent in all_types:
					parents[parent] = None
				if parent not in children.keys() and parent in all_types:
					children[parent] = []
				
				if parent in all_types:
					parents[key] = parent
					children[parent].append(key)

	with open(output_file, 'w') as f:
		if parents.keys() != children.keys():
			print('ERROR')
		for node_type in parents.keys():
			p = convert_biolink_predicate_to_rk(parents[node_type])
			c = [convert_biolink_predicate_to_rk(child) for child in children[node_type]]
			node_type = convert_biolink_predicate_to_rk(node_type)
			f.write('{}\t{}\t{}\n'.format(node_type, p, ",".join(c)))

def convert_rk_predicate_to_biolink(name):
	result = name.split(':')[1]
	result = result.replace('_', ' ')

	return result

def convert_biolink_predicate_to_rk(name):
	if name is None:
		return None

	result = 'biolink:' + name.replace(' ', '_')

	return result


if __name__ == '__main__':
	get_entity_type_hierarchy(input_file, 'entity_' + output_file)
	get_predicate_hierarchy(input_file, 'predicate_' + output_file)