
def map_ids(input_file, output_file, id_mapping_file):
	id_mappings = {}
	with open(id_mapping_file, 'r') as f:
		for line in f:
			old, new = line.strip().split('\t')
			id_mappings[old] = new

	missed = 0
	with open(input_file, 'r') as f1:
		with open(output_file, 'w') as f2:
			for line in f1:
				facts = line.strip().split('\t\t')
				new_facts = []
				for fact in facts:
					s, p, o = fact.split('\t')
					if s not in id_mappings.keys():
						missed += 1
						print('missed s', s)
					if o not in id_mappings.keys():
						missed += 1
						print('missed o', o)
					new_facts.append(f"{id_mappings[s]}\t{p}\t{id_mappings[o]}")

				new_facts = '\t\t'.join(new_facts)

				f2.write(f"{new_facts}\n")


if __name__ == '__main__':
	input_file = '../ExplanationGeneration/samples/robokop2-2_large/contra_false_alternatives2_with_treats_as_pred_old_ids.txt'  # alternatives.txt'
	output_file = '../ExplanationGeneration/samples/robokop2-2_large/contra_false_alternatives2_with_treats_as_pred.txt'
	id_mapping_file = 'samples/robokop2-2_large/robokop2-2_to_rk2-2large_id_mappings.txt'
	map_ids(input_file, output_file, id_mapping_file)
