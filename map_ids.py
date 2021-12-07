
def map_ids(input_file, output_file, id_mapping_file):
	id_mappings = {}
	with open(id_mapping_file, 'r') as f:
		for line in f:
			old, new = line.strip().split('\t')
			id_mappings[old] = new

	with open(input_file, 'r') as f1:
		with open(output_file, 'w') as f2:
			for line in f1:
				facts = line.strip().split('\t\t')
				new_facts = []
				for fact in facts:
					s, p, o = fact.split('\t')
					new_facts.append(f"{id_mappings[s]}\t{p}\t{id_mappings[o]}")

				new_facts = '\t\t'.join(new_facts)

				f2.write(f"{new_facts}\n")


if __name__ == '__main__':
	input_file = 'samples/robokop2/facts.txt'  # alternatives.txt'
	output_file = 'samples/robokop2/facts_sample.txt'
	id_mapping_file = 'samples/robokop2/robokop2_to_rk2sample_id_mappings.txt'
	map_ids(input_file, output_file, id_mapping_file)
