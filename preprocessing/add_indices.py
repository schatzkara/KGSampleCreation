from constants import *
from file_reading.read_relations import read_relations

rel_query = "MATCH ()-[r]-() RETURN DISTINCT type(r)"
rels = list(GRAPH.run(rel_query))
rels = [r[0] for r in rels]

prop_query_sub = "MATCH (e)-[:`{}`]-{}() SET e.{}_sub=True"
index_query_sub = "CREATE INDEX {}_sub FOR (e:named_thing) ON (e.{}_sub)"
prop_query_obj = "MATCH ()-[:`{}`]-{}(e0) SET e0.{}_obj=True"
index_query_obj = "CREATE INDEX {}_obj FOR (e:named_thing) ON (e.{}_obj)"

drop_query_sub = "DROP INDEX {}_sub"
drop_query_obj = "DROP INDEX {}_obj"

for r in rels:
	arrow = '' if r in GRAPH.symm_rels else '>'

	try:
		GRAPH.run(prop_query_sub.format(r, arrow, r))
		GRAPH.run(index_query_sub.format(r, r))
	except:
		print(f'failed at {r} sub index')

	try:
		GRAPH.run(prop_query_obj.format(r, arrow, r))
		GRAPH.run(index_query_obj.format(r, r))
	except:
		print(f'failed at {r} obj index')

	# GRAPH.run(drop_query_sub.format(r))
	# GRAPH.run(drop_query_obj.format(r))

	print(r)
