from constants import *

def get_ontological_relations(graph, output_file=None):
	result = list(graph.run("MATCH (:Concept)-[r]-(:Concept) RETURN DISTINCT type(r)"))
	ontological_relations = [str(r[0]) for r in result]
	# print(ontological_relations)

	result = list(graph.run('MATCH (e)-[r]-(f) WHERE labels(e)<>["Concept"] AND labels(f)<>["Concept"] RETURN DISTINCT type(r)'))
	non_ontological_relations = [str(r[0]) for r in result]

	# for rel in non_ontological_relations:
	# 	if rel in ontological_relations:
	# 		ontological_relations.remove(rel)
	ontological_relations = [rel for rel in ontological_relations if rel not in non_ontological_relations]

	ontological_relations.sort()

	if output_file is not None:
		with open(output_file, 'w') as f:
			for rel in ontological_relations:
				f.write('{}\n'.format(rel))

	return ontological_relations

def get_ontological_entities(graph, output_file=None):
	result = list(graph.run("MATCH (e:Concept) RETURN DISTINCT id(e)"))
	ontological_entities = [int(r[0]) for r in result]

	if output_file is not None:
		with open(output_file, 'w') as f:
			for ent in ontological_entities:
				f.write('{}\n'.format(ent))

	return ontological_entities


if __name__ == '__main__':
	get_ontological_entities(GRAPH, 'ontological_entities.txt')