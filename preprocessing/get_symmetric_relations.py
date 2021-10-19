import yaml

input_file = 'C://Users//Kara//Documents//Research//ExternalSourceCode//biolink-model//biolink-model.yaml'
output_file = 'symmetric_relations.txt'


def get_symmetric_relations(input_file, output_file):
	"""Extracts all the symmetric relation from the biolink yaml file.
	:param input_file: (str) the biolink yaml file where the symmetric relations are stored
	:param output_file: (str) the file where the extracted symmetric relations should be written
	"""
	symmetric_relations = []

	with open(input_file, encoding='utf-8') as f:
		model = yaml.full_load(f)  # load(f, Loader=yaml.FullLoader)

		slots = model['slots']

		skip = True
		for key in slots.keys():
			# if key == 'related to':
			# 	skip = False

			# if skip:
			# 	continue

			if 'symmetric' in slots[key].keys():
				print(key)
				symmetric_relations.append(key.replace(' ', '_'))

	with open(output_file, 'w') as f:
		for rel in symmetric_relations:
			f.write(rel)
			f.write('\n')


if __name__ == '__main__':
	get_symmetric_relations(input_file, output_file)



'''related to
interacts with
physically interacts with
genetic association
similar to'''
