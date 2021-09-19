import os
import py2neo

from file_reading.read_domain_range import read_domain_range_2
from file_reading.read_symmetric_relations import read_symmetric_relations
from file_reading.read_relations import read_relations
from file_reading.read_type_hierarchy import read_type_hierarchy


class Knowledge_Graph:
	def __init__(self, name='robokop'):
		self.name = name
		# necessary data files from preprocessing
		# self.dr_file = os.path.join('data_files', self.name, 'refined_domain_range_2.csv')
		self.symm_file = os.path.join('data_files', self.name, 'symmetric_relations.txt')
		# self.onto_file = os.path.join('data_files', self.name, 'ontological_relations.txt')
		self.entity_type_hierarchy_file = os.path.join('data_files', self.name, 'entity_type_hierarchy.txt')
		self.predicate_hierarchy_file = os.path.join('data_files', self.name, 'predicate_type_hierarchy.txt')
		# self.rel_exist_prob_file = os.path.join('data_files', self.name, 'relation_existence_probs.csv')

		# the connection to neo4j
		host = 'localhost'
		port = 7687
		user = 'neo4j'
		password = 'password'
		self.graph = py2neo.Graph(host=host, port=port, user=user, password=password)
		# self.graph = py2neo.Graph(host='robokopdb1.renci.org', port=7687, user='neo4j', password='ncatsgamma')

		# the graph size
		self.graph_size = None  # int(list(self.run('MATCH ()-[r]-() RETURN COUNT(*)'))[0]['COUNT(*)'])  # 14,695,902 ... 32,442,448

		# read in preprocessed data from files
		self.symm_rels = read_symmetric_relations(self.symm_file)
		# self.onto_rels = read_relations(self.onto_file)
		self.entity_type_parents, self.entity_type_children = read_type_hierarchy(self.entity_type_hierarchy_file)
		self.predicate_parents, self.predicate_children = read_type_hierarchy(self.predicate_hierarchy_file)
		# self.rels, self.inputs, self.ranges = read_domain_range_2(self.dr_file, self.symm_file)
		# self.rels.sort()
		# # ignore 'Unmapped_Relation' and 'named_thing' because these are not interesting for inferences
		# if 'Unmapped_Relation' in self.rels:
		# 	self.rels.remove('Unmapped_Relation')
		# 	self.inputs.remove('Unmapped_Relation')
		# 	self.ranges.remove('Unmapped_Relation')
		# for r in self.rels: 
		# 	if 'named_thing' in self.inputs[r]:
		# 		self.inputs[r].remove('named_thing')
		# 	self.ranges[r].pop('named_thing', None)
		# self.parents['Concept'] = None
		# self.children['Concept'] = []

	def size(self):
		if self.graph_size is None:
			self.graph_size = int(list(self.run('MATCH ()-[r]->() RETURN COUNT(*)'))[0]['COUNT(*)'])  # 14,695,902 ... 32,442,448
			
		return self.graph_size

	def run(self, query):
		# print(query)
		# input()
		# return 
		try:
			result = self.graph.run(query)
			# print(result)
			return result
		except py2neo.database.work.TransientError as e:
			print(e)
			print(query)
		except:
			print(query)
			print('FAILED')
			return None
