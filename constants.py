
from Knowledge_Graph import Knowledge_Graph

# the knowledge graph in use
KG = 'robokop2'  # 'robokop' or 'drkg'
GRAPH = Knowledge_Graph(KG)
SAMPLE = 'rw5mil'
INDICES = True

# # the rule set(s)
# RULES_DIR = 'rules/'
# # RULES = read_iris_rules(RULES_FILE, has_weights=True)

# # constants for whether a relation is directed from or directed to an entity
# FROM = True
# TO = False

# # constants for interpretation of type hierarchy
# COMPLETELY_TYPED = True  # we assume that all entities are labeled as specifically as possible
# INHERITABLE = False  # we assume that entities labeled by a certain parent class can be further classified
# TYPE_HIERARCHY = COMPLETELY_TYPED

# # constants for confidence measure
# STANDARD = 0
# SOFT = 1
# SOFTER = 2
# CONFIDENCE = STANDARD

# PROBLOG = 0
# EXFAKT = 1
# CONF = 2
# HC = 3
# F1 = 4

# # constants for dataset splits
# SPLIT = 40
# TRAINING = 0
# TESTING = 1
# NEITHER = 2
# # SETTING = TRAINING

# # the number of arguments to the driver
# # setting is a required argument 
# # if setting is TESTING, then file_name is a required argument
# # otherwise, head_rel and path_length are required arguments and
# # direct, entity_types, treatable_only, and mirror are optional arguments
# MIN_ARGS = 5
# MAX_ARGS = 5
# # ARG_COUNT = 7
