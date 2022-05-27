# KGSampleCreation main script
import os
from kg_to_txt import kg_to_txt, duplicate_symm_rels
from graph_sampling import random_walk
from get_node_types import make_types_file
from add_negative_predicate import generate_negative_predicate, add_negative_predicates_to_neo4j
from get_experimental_data import get_hypothesized_facts_txt, get_negative_examples
from mark_subset_in_neo4j import mark_subset_in_neo4j

KG = 'robokop2-2'

OUTPUT_DIR = f'samples/{KG}_large'

KG_FILE_NAME = f'{KG}_singular_symm_rels.txt'

SAMPLE_NAME = 'wo_test'
SAMPLE_FILE_NAME = 'sample.txt'
DESIRED_SIZE = 11000000
RELS_TO_AVOID = []
ENTITIES_TO_AVOID = []

TYPES_FILE = f'{KG}_entity_types.txt'  # 'robokop_sample_entity_types.txt'

NEGATIVES_FILE = 'sample_generated_negatives.txt'
SAMPLE_WITH_NEGS_FILE = 'sample_with_negs.txt'
PREDICATE = 'biolink:treats'
NUM_NEGS_PER_POS = 1
ADD_NEGS_TO_NEO4J = False

SAMPLE_WO_TEST_FILE = 'sample_with_negs_wo_test_data.txt'
FACTS_FILE = 'facts.txt'
ALTS_FILE = 'alternatives.txt'
NUM_POS_FACTS = 250
NUM_ALTS_PER_POS = 5

SAMPLE_WO_TEST_FILE2 = 'sample_with_negs_wo_test_data2.txt'
FACTS_FILE2 = 'other_facts.txt'
ALTS_FILE2 = 'other_alternatives.txt'
NUM_POS_FACTS2 = 250
NUM_ALTS_PER_POS2 = 1

SAMPLE_WITH_DUPLCIATE_SYMM_RELS = 'sample_duplicate_symm_rels.txt'


# os.mkdir(OUTPUT_DIR)
KG_FILE_NAME = os.path.join(OUTPUT_DIR, KG_FILE_NAME)
SAMPLE_FILE_NAME = os.path.join(OUTPUT_DIR, SAMPLE_FILE_NAME)
TYPES_FILE = os.path.join(OUTPUT_DIR, TYPES_FILE)
NEGATIVES_FILE = os.path.join(OUTPUT_DIR, NEGATIVES_FILE)
SAMPLE_WITH_NEGS_FILE = os.path.join(OUTPUT_DIR, SAMPLE_WITH_NEGS_FILE)
SAMPLE_WO_TEST_FILE = os.path.join(OUTPUT_DIR, SAMPLE_WO_TEST_FILE)
FACTS_FILE = os.path.join(OUTPUT_DIR, FACTS_FILE)
ALTS_FILE = os.path.join(OUTPUT_DIR, ALTS_FILE)
SAMPLE_WO_TEST_FILE2 = os.path.join(OUTPUT_DIR, SAMPLE_WO_TEST_FILE2)
FACTS_FILE2 = os.path.join(OUTPUT_DIR, FACTS_FILE2)
ALTS_FILE2 = os.path.join(OUTPUT_DIR, ALTS_FILE2)
SAMPLE_WITH_DUPLCIATE_SYMM_RELS = os.path.join(OUTPUT_DIR, SAMPLE_WITH_DUPLCIATE_SYMM_RELS)


if __name__ == '__main__':
	# '''
	# Random walk must be done on KG WITHOUT duplicated symmetric relations
	# Rule mining must be done on KG WITH duplicated symmetric relations

	# Steps:
	# 1. Use kg_to_txt.py to create a .txt version of the KG without duplicated symmetric relations
	'''kg_to_txt(KG_FILE_NAME, duplicate_symm_rels=False)
				print('Completed step 1.')'''
	# quit()
	# 2. Use graph_sampling.py to generate a subset of the graph of the desired size
	random_walk(KG_FILE_NAME, SAMPLE_FILE_NAME, desired_size=DESIRED_SIZE, rels_to_avoid=RELS_TO_AVOID, entities_to_avoid=ENTITIES_TO_AVOID)
	print('Completed step 2.')

	# 3. Use get_node_types.py to create a .txt file of the node types
	'''make_types_file(SAMPLE_FILE_NAME, TYPES_FILE)
				print('Completed step 3.')'''

	# 4. Use add_negative_predicate.py to generate n negative triples for each positive triple of each predicate desired AND (optionally) add the negative triples to the neo4j version of the KG
	generate_negative_predicate(SAMPLE_FILE_NAME, TYPES_FILE, NEGATIVES_FILE, predicate=PREDICATE, n=NUM_NEGS_PER_POS)

	with open(SAMPLE_WITH_NEGS_FILE, 'w') as f:
		with open(SAMPLE_FILE_NAME, 'r') as g:
			lines = g.readlines()
			f.writelines(lines)
		with open(NEGATIVES_FILE, 'r') as g:
			lines = g.readlines()
			f.writelines(lines)
	
	if ADD_NEGS_TO_NEO4J:
		add_negative_predicates_to_neo4j(NEGATIVES_FILE) # does the sample need to be marked here????
	print('Completed step 4.')

	# 5. Use get_experimental_data.py to generate n candidiate facts and m alternative facts for each candidate fact
	# 6. Remove the candidates and alternatives from the sample
	get_hypothesized_facts_txt(SAMPLE_WITH_NEGS_FILE, SAMPLE_WO_TEST_FILE, FACTS_FILE, PREDICATE, NUM_POS_FACTS)
	get_negative_examples(SAMPLE_WITH_NEGS_FILE, TYPES_FILE, FACTS_FILE, ALTS_FILE, NUM_ALTS_PER_POS)
	get_hypothesized_facts_txt(SAMPLE_WO_TEST_FILE, SAMPLE_WO_TEST_FILE2, FACTS_FILE2, PREDICATE, NUM_POS_FACTS2)
	# '''
	get_negative_examples(SAMPLE_WO_TEST_FILE, TYPES_FILE, FACTS_FILE2, ALTS_FILE2, NUM_ALTS_PER_POS2)
	print('Completed step 5 and 6.')

	# '''
	# 8. Use mark_subset_in_neo4j.py to mark all triples in the subset in Neo4j
	'''mark_subset_in_neo4j(SAMPLE_WO_TEST_FILE2, SAMPLE_NAME, clear_previous=False)
				print('Completed step 8.')'''

	# 7. Use kg_to_txt.py to duplicate the symmetric relations in this sample
	duplicate_symm_rels(SAMPLE_WO_TEST_FILE2, SAMPLE_WITH_DUPLCIATE_SYMM_RELS)
	print('Completed step 7.')	
	

	# instead, create sample in a new neo4j database????
	# '''
