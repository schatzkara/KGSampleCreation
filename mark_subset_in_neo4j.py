from constants import *
import sys

def mark_subset_in_neo4j(subset_file, subset_name, clear_previous):
	if clear_previous:
		clear_previous_subset()

	count = 0
	with open(subset_file, 'r') as f:
		skip = False
		for line in f:
			if count < 1219000:
				count += 1
				continue
			if skip:
				skip = False
				continue
			else:
				s, p, o = line.strip().split('\t')
				# if p in GRAPH.symm_rels:
				# 	skip = True

				rel = list(GRAPH.run("MATCH (e)-[r:`{}`]->(f) WHERE id(e)={} AND id(f)={} SET r.sample='{}' RETURN r".format(p, s, o, subset_name)))
				# print(rel)
				if len(rel) <= 0:
					print('failed on {} {} {}'.format(s, p, o))

				count += 1
				if count % 1000 == 0:
					print(count)

	print('{} edges were marked'.format(count))

	nodes = list(GRAPH.run("MATCH (e)-[r]->() WHERE r.sample='{}' SET e.sample='{}' RETURN e".format(subset_name, subset_name)))

	print('{} nodes were marked'.format(len(nodes)))

def clear_previous_subset():
	# result = list(GRAPH.run("MATCH ()-[r]->() SET r.sample=null"))
	result = list(GRAPH.run("MATCH ()-[r]->() DELETE r.sample"))

	print('edges were unmarked')

def mark_drkg_subset_in_neo4j(treats_triple_file, subset_name):
	# complete = ['treats','CLEAVAGE_REACTION','DEPHOSPHORYLATION_REACTION','UBIQUITINATION_REACTION','PROTEIN_CLEAVAGE',
	# 			'ADP_RIBOSYLATION_REACTION','Disease_resembles_Disease','biomarkers_of_disease_progression','ALLOSTERIC_MODULATOR',
	# 			'Coronavirus_ass_host_gene','VirGenHumGen','drug_targets','CHANNEL_BLOCKER','ANTIBODY','enhances_response','Covid2_acc_host_gene',
	# 			'mutations_affecting_disease_course','BLOCKER','same_protein_or_complex','Pharmacologic_Class_includes_Compound','antagonism',
	# 			'BINDER','Disease_localizes_Anatomy','EXPRESSION','PTMOD','PHOSPHORYLATION_REACTION','PARTIAL_AGONIST','Compound_binds_Gene','agonism',
	# 			'OSITIVE_ALLOSTERIC_MODULATOR','ACTIVATOR','carrier','enzyme','possible_therapeutic_effect','Compound_downregulates_Gene',
	# 			'Compound_palliates_Disease','Compound_treats_Disease','DrugVirGen','HumGenHumGen','biomarkers_diagnostic',
	# 			'Disease_presents_Symptom','alleviates','prevents','inhibits_cell_growth_esp_cancers','overexpression_in_disease','DrugHumGen',
	# 			'increases_expression_production','side_effect_adverse_event','Compound_resembles_Compound','AGONIST',
	# 			'treatment_therapy_including_investigatory','promotes_progression','signaling_pathway','causal_mutations','ANTAGONIST',
	# 			'target','Compound_upregulates_Gene','MODULATOR','INHIBITOR']
	# incomplete = ["Anatomy_upregulates_Gene","BINDING_STRING","CATALYSIS","Compound_causes_Side_Effect","Gene_interacts_Gene","Gene_participates_Biological_Process",
	# 			"Gene_participates_Cellular_Component","Gene_participates_Molecular_Function","Gene_participates_Pathway","Gene_regulates_Gene","PHYSICAL_ASSOCIATION",
	# 			"REACTION","ddi_interactor_in"]
	predicates = list(GRAPH.run("MATCH ()-[r]->() RETURN type(r), COUNT(*) ORDER BY COUNT(*)"))

	# predicates.reverse()

	for p in predicates:
		# print(p[0])
		# print(type(p[0]))
		# quit()
		if p[0] in incomplete:
			count = list(GRAPH.run(f"MATCH ()-[r:{p[0]}]-() RETURN COUNT(*)"))
			rels = list(GRAPH.run(f"MATCH ()-[r:{p[0]}]-() SET r.sample='{subset_name}' RETURN r"))

			print(p[0])
			print(f'marked {len(rels)} out of {int(count[0][0])}')

	# count = 0
	# with open(treats_triple_file, 'r') as f:
	# 	skip = False
	# 	for line in f:
	# 		if skip:
	# 			skip = False
	# 			continue
	# 		else:
	# 			s, p, o = line.strip().split('\t')
	# 			if p in GRAPH.symm_rels:
	# 				skip = True

	# 			rel = list(GRAPH.run("MATCH (e)-[r:{}]->(f) WHERE id(e)={} AND id(f)={} SET r.sample='{}' RETURN r".format(p, s, o, subset_name)))

	# 			if len(rel) <= 0:
	# 				print('failed on {} {} {}'.format(s, p, o))

	# 			count += 1
	# 			if count % 1000 == 0:
	# 				print(count)

def mark_large_predicates_drkg(predicate, subset_name, start, split):
	subjects = list(GRAPH.run(f'MATCH (e)-[r:{predicate}]->() WHERE r.sample is null RETURN id(e), COUNT(*) ORDER BY COUNT(*) DESC'))
	objects = list(GRAPH.run(f'MATCH ()-[r:{predicate}]->(e) WHERE r.sample is null RETURN id(e), COUNT(*) ORDER BY COUNT(*) DESC'))

	# if split != 0:
	subjects = subjects[start:len(subjects)-1:split]
	objects = objects[start:len(objects)-1:split]

	if len(subjects) < len(objects):
		count = 0
		for s in subjects:
			rels = list(GRAPH.run(f"MATCH (e)-[r:{predicate}]->() WHERE id(e)={int(s[0])} AND r.sample is null SET r.sample='{subset_name}' RETURN r"))

			# print(predicate)
			if len(rels) != int(s[1]):
				print(f'marked {len(rels)} out of {int(s[1])} for subject {s[0]}')

			count += 1
			if count % 10 == 0:
				print(f'{count}/{len(subjects)}')
	else: 
		count = 0
		for s in objects:
			rels = list(GRAPH.run(f"MATCH ()-[r:{predicate}]->(e) WHERE id(e)={int(s[0])} AND r.sample is null SET r.sample='{subset_name}' RETURN r"))

			# print(predicate)
			if len(rels) != int(s[1]):
				print(f'marked {len(rels)} out of {int(s[1])} for object {s[0]}')

			count += 1
			if count % 10 == 0:
				print(f'{count}/{len(objects)}')

	


if __name__ == '__main__':
	# mark_subset_in_neo4j('working_sample/complete_sample.txt', 'rw4mil', clear_previous=False)
	# mark_subset_in_neo4j('drkg_sample/drkg_complete_sample.txt', 'wo_test', clear_previous=False)
	# mark_drkg_subset_in_neo4j('drkg_treats_in_sample.txt', 'wo_test')

	# parse arguments
	script_name, predicate, start, split = sys.argv[0], sys.argv[1], int(sys.argv[2]), int(sys.argv[3])

	mark_large_predicates_drkg(predicate, 'wo_test', start=start, split=split)
