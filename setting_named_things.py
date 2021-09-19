from constants import *

gene_keys = list(GRAPH.run("MATCH (e:Gene) RETURN keys(e), COUNT(*)"))

key_counts = {}
for keys, count in gene_keys:
	for k in keys:
		if k not in key_counts.keys():
			key_counts[k] = 0
		key_counts[k] += count

key_counts = dict(sorted(key_counts.items(), key=lambda x: x[1]))

for k in ['type', 'name', 'reference', 'id', 'source']:
	key_counts.pop(k)

count = 0
for key in key_counts.keys():
	list(GRAPH.run(f"MATCH (e:Gene) WHERE e.{key}=True SET e:named_thing RETURN COUNT(*)"))
	count += 1

	print(f'{count}/{len(key_counts.keys())}')

