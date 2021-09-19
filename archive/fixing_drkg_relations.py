from constants import *

# ids = list(GRAPH.run("MATCH (m)-[rel:`Gene_participates_Biological Process`]->(n)  RETURN DISTINCT id(n),COUNT(*) ORDER BY COUNT(*) DESC"))

# for i in ids:
# 	print(list(GRAPH.run(f"MATCH (m)-[rel:`Gene_participates_Biological Process`]->(n) WHERE id(n)={i[0]} WITH rel CALL apoc.refactor.setType(rel,'Gene_participates_Biological_Process') YIELD input, output RETURN COUNT(*)")))

rels = list(GRAPH.run("MATCH ()-[r]->() RETURN DISTINCT type(r)"))

for r in rels:
	old_name = r[0]
	new_name = old_name

	if '(' in new_name:
		new_name = new_name.replace('(', '')
	if ')' in new_name:
		new_name = new_name.replace(')', '')
	if '/' in new_name:
		new_name = new_name.replace('/', '_')

	if new_name != old_name:
		print(new_name)

		print(list(GRAPH.run(f"MATCH (m)-[rel:`{old_name}`]->(n) WITH rel CALL apoc.refactor.setType(rel,'{new_name}') YIELD input, output RETURN COUNT(*)")))


