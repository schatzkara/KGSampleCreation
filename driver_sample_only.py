# KGSampleCreation main script
import os
import time
from kg_to_txt import kg_to_txt, duplicate_symm_rels
from graph_sampling import random_walk
from get_node_types import make_types_file

OUTPUT_DIR = 'samples/robokop2-2'

KG_FILE_NAME = 'robokop2-2_singular_symm_rels.txt'

SAMPLE_FILE_NAME = 'robokop2-2sample4.txt'
DESIRED_SIZE = 5000000
RELS_TO_AVOID = []
ENTITIES_TO_AVOID = []

# TYPES_FILE = 'robokop2-2_sample_entity_types.txt'  # 'robokop_sample_entity_types.txt'

# os.mkdir(OUTPUT_DIR)
KG_FILE_NAME = os.path.join(OUTPUT_DIR, KG_FILE_NAME)
# SAMPLE_FILE_NAME = os.path.join(OUTPUT_DIR, SAMPLE_FILE_NAME)
# TYPES_FILE = os.path.join(OUTPUT_DIR, TYPES_FILE)


if __name__ == '__main__':
	start = time.time()
	# '''
	# Random walk must be done on KG WITHOUT duplicated symmetric relations
	# Rule mining must be done on KG WITH duplicated symmetric relations

	# Steps:
	'''
	# 1. Use kg_to_txt.py to create a .txt version of the KG without duplicated symmetric relations
	kg_to_txt(KG_FILE_NAME, duplicate_symm_rels=False)
	print('Completed step 1.')
	'''

	for x in range(19,21):
		SAMPLE_FILE_NAME = f'robokop2-2sample{x}.txt'

		# 2. Use graph_sampling.py to generate a subset of the graph of the desired size
		random_walk(KG_FILE_NAME, SAMPLE_FILE_NAME, desired_size=DESIRED_SIZE, rels_to_avoid=RELS_TO_AVOID, entities_to_avoid=ENTITIES_TO_AVOID, verbose=False)
		print('Completed step 2.')

		'''
		# 3. Use get_node_types.py to create a .txt file of the node types
		make_types_file(SAMPLE_FILE_NAME, TYPES_FILE)
		print('Completed step 3.')
		'''

		finish = time.time()
		print(finish - start)

		time.sleep(120)
