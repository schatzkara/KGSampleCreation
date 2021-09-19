import csv
import os

from file_reading.read_relations import read_relations

def format_AMIE_to_iris(file_name, output_file, append=False, include_weights=False, weight_threshold=0, conf_threshold=0.00, hc_threshold=0.0, rules_per_head=None, rels_to_avoid=[]):
	rules_list = []
	rule_confidences = {}
	with open(file_name, 'r') as f:
		for line in f:
			if not line[0].startswith('?'):
				continue
			# rule, hc, std_conf, pca_conf, pos_ex, body_size, PCA_body_size, func_var, std_lower_bound, pca_lower_bound, conf_estimation = line.strip().split('\t')
			rule, hc, std_conf, pca_conf, pos_ex, body_size, PCA_body_size, func_var = line.strip().split('\t')

			if float(std_conf) < conf_threshold or int(pos_ex) < weight_threshold or float(hc) < hc_threshold:
				# print('conf')
				# print(std_conf)
				continue

			rule_body, rule_head = rule.strip().split('=>')

			entity_mappings = {}
			entity_count = 0

			e0, head_rel, en = rule_head.strip().split('  ')

			if head_rel in rels_to_avoid:
				# print('head')
				continue
			
			rule_line = '{}({},{}):- '.format(head_rel, e0, en)

			rule_parts = rule_body.strip().split('  ')
			triples = [(rule_parts[i], rule_parts[i+1], rule_parts[i+2]) for i in range(0, len(rule_parts), 3)]

			atoms = []
			avoid = False
			for t in triples:
				s, p, o = t

				if p in rels_to_avoid:
					# print('body', p)
					avoid = True
					break

				rule_line += '{}({},{}), '.format(p, s, o)

			if avoid:
				continue

			rule_line = rule_line[:-2] + '.'
			
			if include_weights:
				rule_line = '{}\t{}'.format(std_conf, rule_line)

			rules_list.append(rule_line)

			if head_rel not in rule_confidences.keys():
				rule_confidences[head_rel] = {}
			rule_confidences[head_rel][rule_line] = float(std_conf)
			# print('added a rule!')

			# print(body_size)

	sorted_rules = {}
	for head_rel in rule_confidences.keys():
		sorted_rules[head_rel] = [x[0] for x in sorted(rule_confidences[head_rel].items(), key=lambda x: x[1], reverse=True)]
		# print(sorted_rules[head_rel])
		# input()

	mode = 'a' if append else 'w'
	with open(output_file, mode) as f:
		for head_rel, rules in sorted_rules.items():
			cutoff = len(rules) if rules_per_head is None else min(len(rules), rules_per_head)
			# cutoff = len(rules)
			# if rules_per_head is not None and rules_per_head < cutoff:
			# 	cutoff = rules_per_head
			for i in range(cutoff):
				f.write(rules[i])
				f.write('\n')
		# for r in rules_list:
		# 	f.write(r)
		# 	f.write('\n')


if __name__ == '__main__':
	# file_name = 'amie_training_output.txt'
	dir_name = 'working_sample/amie_rules/'
	files = os.listdir(dir_name)
	files = [os.path.join(dir_name, f) for f in files]
	# files = ['rules/not_treats_rules.txt']

	rels_to_avoid = set(read_relations('data_files/robokop/ontological_relations.txt'))
	# rels_to_avoid.update(read_relations('data_files/robokop/non_prevalent_rels_1.txt'))
	# rels_to_avoid.remove('treats')

	# print(rels_to_avoid)

	output_file = 'all_rules_weight_25_20_per_head.iris'
	for f in files:
		format_AMIE_to_iris(f, output_file, append=True, include_weights=True, weight_threshold=25, conf_threshold=0.0, hc_threshold=0.0, rules_per_head=20, rels_to_avoid=rels_to_avoid)
