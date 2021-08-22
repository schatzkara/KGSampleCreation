# KGSampleCreation

Random walk must be done on KG WITHOUT duplicated symmetric relations
Rule mining must be done on KG WITH duplicated symmetric relations

Steps:
1. Use kg_to_txt.py to create a .txt version of the KG without duplicated symmetric relations
2. Use graph_sampling.py to generate a subset of the graph of the desired size
2. Use get_node_types.py to create a .txt file of the node types
3. Use add_negative_predicate.py to generate n negative triples for each positive triple of each predicate desired AND (optionally) add the negative triples to the neo4j version of the KG
4. Use get_experimental_data.py to generate n candidiate facts and m alternative facts for each candidate fact
5. Remove the candidates and alternatives from the sample
6. Use kg_to_txt.py to duplicate the symmetric relations in this sample

