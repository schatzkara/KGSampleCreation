# from patterns.Atom import Atom

def read_facts(file):
	facts = []
	with open(file, 'r') as f:
		for line in f:
			s, p, o = line.strip().split('\t')
			facts.append((s, p, o))

	return facts

# def read_test_data(file):
# 	fact_sets = {}
# 	with open(file, 'r') as f:
# 		for line in f:
# 			facts = line.strip().split('\t\t')
# 			pos, negs = facts[0], facts[1:]
# 			s, p, o = pos.split('\t')
# 			pos = Atom(s, p, o)

# 			fact_sets[str(pos)] = []
# 			for fact in facts:
# 				s, p, o = fact.split('\t')
# 				fact_sets[str(pos)].append(Atom(s, p, o))

# 	return fact_sets
