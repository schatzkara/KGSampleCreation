from constants import *

predicates = list(GRAPH.run("MATCH ()-[r]->() RETURN DISTINCT TYPE(r), COUNT(*)"))
predicates.sort(key=lambda x: int(x[1]))
predicates = [p[0] for p in predicates]

for p in predicates:
	duplicates = list(GRAPH.run(f"MATCH (e)-[r:`{p}`]->(f) WITH id(e) as e, id(r) as r, id(f) as f MATCH (e1)-[r1:`{p}`]->(f1) WHERE e=id(e1) AND f=id(f1) AND r<id(r1)AND r1.sample='rw5mil' RETURN COUNT(*)"))
	print(f'{duplicates[0][0]}\t{p}')
