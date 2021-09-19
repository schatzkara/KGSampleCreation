import sys
import csv
from py2neo import Graph

# from constants import *

def get_standard_domain_range(file_name):
   """Gets the domains and ranges of each relation in ROBOKOP following the standard definitions of domain and range.
   :param file_name: (str) the file to write the domains and ranges
   """
   g = Graph(host='robokopdb1.renci.org', port=7687, user='neo4j', password='ncatsgamma')

   rel_query = "MATCH ()-[r]-() RETURN DISTINCT type(r)"
   matches = g.run(rel_query)
   rels = list(matches)
   rels = [x.values()[0] for x in rels if x.values()[0]!=None]
   rels.sort()
   print(rels)
   print(len(rels))
   sys.stderr.write("%s.\n" % ' '.join(rels))

   with open(file_name, mode='w') as output_file:
      writer = csv.writer(output_file, delimiter=',', lineterminator='\r')
      writer.writerow(['RELATIONSHIP_TYPE', 'DOMAIN', 'RANGE'])

      print("RELATIONSHIP_TYPE| DOMAIN| RANGE")
      for rel in rels:
         sys.stderr.write("Relationship %s in progress.\n" % rel)
         query = "MATCH (n)-[r:%s]->(m) RETURN DISTINCT LABELS(n)" % rel
         rel_domain = set()
         rel_range = set()

         matches = g.run(query)
         for m in matches:
            rel_domain.update(m.values()[0])

         query = "MATCH (n)-[r:%s]->(m) RETURN DISTINCT LABELS(m)" % rel

         matches = g.run(query)
         for m in matches:
            rel_range.update(m.values()[0])

         # print("%s| %s| %s" % (rel, ",".join(sorted(rel_domain)), ",".join(sorted(rel_range))))
         writer.writerow([rel, ','.join(sorted(rel_domain)), ','.join(sorted(rel_range))])

def get_refined_domain_range(file_name):
   """Gets the domains and ranges of each relation in ROBOKOP following the refined definitions of domain and input specific range.
   This is a worse format than the method above.
   :param file_name: (str) the file to write the domains and ranges
   """
   # g = Graph(host='robokopdb1.renci.org', port=7687, user='neo4j', password='ncatsgamma')
   g = GRAPH  # Graph(host='localhost', port=7687, user='neo4j', password='password')

   schema_query = "MATCH (x)-[r]->(y) RETURN DISTINCT labels(x), type(r), labels(y), count(*)"  # LIMIT 10"
   matches = list(g.run(schema_query))

   # dictionary with relation types as keys
   # values are dictionaries with input types as keys and ranges as values
   ranges = {}

   for m in matches:
      x, r, y, count = m

      if 'named_thing' in x and len(x) > 1:
         x.remove('named_thing')
      if 'named_thing' in y and len(y) > 1:
         y.remove('named_thing')

      if r not in ranges.keys():
         ranges[r] = {}

      for i in x:
         if i not in ranges[r].keys():
               ranges[r][i] = set()

      for i in x:
            ranges[r][i].update(set(y))

   print(ranges)

   with open(file_name, mode='w') as output_file:
      writer = csv.writer(output_file, delimiter=',',lineterminator='\r')
      writer.writerow(['RELATIONSHIP_TYPE', 'INPUT', 'RANGE'])

      for rel, rel_range in ranges.items():
         for rel_input, input_range in rel_range.items():
            writer.writerow([rel, rel_input, ','.join(sorted(input_range))])

def get_refined_domain_range_2(file_name):
   """Gets the domains and ranges of each relation in ROBOKOP following the refined definitions of domain and input specific range.
   This is a better format than the method above.
   :param file_name: (str) the file to write the domains and ranges
   """
   # g = Graph(host='robokopdb1.renci.org', port=7687, user='neo4j', password='ncatsgamma')
   g = GRAPH  # Graph(host='localhost', port=7687, user='neo4j', password='password')

   schema_query = "MATCH (x)-[r]->(y) RETURN DISTINCT labels(x), type(r), labels(y), count(*)"  # LIMIT 10"
   matches = list(g.run(schema_query))

   # dictionary with relation types as keys
   # values are dictionaries with input types as keys and ranges as values
   ranges = {}

   for m in matches:
      x, r, y, count = m
      x, y = ','.join(x), ','.join(y)

      # if 'named_thing' in x and len(x) > 1:
      #    x.remove('named_thing')
      # if 'named_thing' in y and len(y) > 1:
      #    y.remove('named_thing')

      if r not in ranges.keys():
         ranges[r] = {}

      # for i in x:
      if x not in ranges[r].keys():
         ranges[r][x] = set()

      # for i in x:
      ranges[r][x].add(y)

   # for r in ranges.items():
   #    print(r)

   with open(file_name, mode='w') as output_file:
      writer = csv.writer(output_file, delimiter=',',lineterminator='\r')
      writer.writerow(['RELATIONSHIP_TYPE', 'INPUT', 'RANGE'])

      for rel, rel_range in ranges.items():
         for rel_input, input_range in rel_range.items():
            writer.writerow([rel, rel_input, ';'.join(sorted(input_range))])

def get_edge_domain_range(file_name):
   """Gets the domains and ranges of each relation in ROBOKOP where the domains and ranges contain edge types not node types.
   :param file_name: (str) the file to write the domains and ranges
   """
   graph = GRAPH  # Graph(host='localhost', port=7687, user='neo4j', password='password')
   symmetric_relations = SYMM_RELS
   rel_query = "MATCH ()-[r]-() RETURN DISTINCT type(r)"
   matches = graph.run(rel_query)
   rels = list(matches)
   rels = [x.values()[0] for x in rels if x.values()[0] != None]
   rels.sort()
   print(len(rels))

   domain_query = "MATCH ()-[r]-()-[s:{}]-{}() RETURN DISTINCT type(r)"  # LIMIT 10"
   range_query = "MATCH ()-[s:{}]-{}()-[r]-() RETURN DISTINCT type(r)"


   with open(file_name, mode='w') as output_file:
      writer = csv.writer(output_file, delimiter=',', lineterminator='\r')
      writer.writerow(['RELATIONSHIP_TYPE', 'DOMAIN', 'RANGE'])

      print("RELATIONSHIP_TYPE | DOMAIN | RANGE")
      for r in rels:
         arrow = '>' if r in symmetric_relations else ''
         query1 = domain_query.format(r, arrow)
         query2 = range_query.format(r, arrow)

         rel_domain = list(graph.run(query1))
         rel_domain = [x.values()[0] for x in rel_domain if x.values()[0] != None]
         rel_range = list(graph.run(query2))
         rel_range = [x.values()[0] for x in rel_range if x.values()[0] != None]
   
         writer.writerow([r, ','.join(sorted(rel_domain)), ','.join(sorted(rel_range))])

         print(r, rel_domain, rel_range)

def get_entity_domain_range(file_name):
   """Gets the domains and ranges of each relation in ROBOKOP where the domains and ranges contain actual entities not node types.
   :param file_name: (str) the file to write the domains and ranges
   """
   graph = GRAPH
   symmetric_relations = SYMM_RELS
   rel_query = 'MATCH ()-[r]-() RETURN DISTINCT type(r)'
   matches = list(graph.run(rel_query))
   rels = [x.values()[0] for x in matches if x.values()[0] != None]
   rels.sort()
   print(len(rels))
   # print(rels)

   domain_query = 'MATCH (a)-[r:{}]->() RETURN DISTINCT id(a)'
   range_query = 'MATCH ()-[r:{}]->(b) RETURN DISTINCT id(b)'

   with open(file_name, mode='w') as f:
      # writer = csv.writer(f, delimiter=',', lineterminator='\r')
      # writer.writerow(['RELATIONSHIP_TYPE', 'DOMAIN', 'RANGE'])
      f.write('RELATIONSHIP_TYPE\tDOMAIN\tRANGE\n')
      for r in rels:
         query1 = domain_query.format(r)
         query2 = range_query.format(r)

         rel_domain = list(graph.run(query1))
         rel_domain = [str(a) for a in rel_domain]
         rel_range = list(graph.run(query2))
         rel_range = [str(b) for b in rel_range]

         if r in symmetric_relations:
            domain_range = rel_domain + rel_range
            f.write('{}\t{}\t{}\n'.format(r,','.join(sorted(domain_range)),','.join(sorted(domain_range))))
            # writer.writerow([r, ','.join(sorted(domain_range)), ','.join(sorted(domain_range))])
            # print(','.join(sorted(domain_range)))
         else:
            f.write('{}\t{}\t{}\n'.format(r,','.join(sorted(rel_domain)), ','.join(sorted(rel_range))))
            # writer.writerow([r, ','.join(sorted(rel_domain)), ','.join(sorted(rel_range))])
            # print(','.join(sorted(rel_domain)))
            # print(','.join(sorted(rel_range)))
         print(r)


if __name__ == "__main__":
   # file_name = 'refined_domain_range.csv'
   # get_refined_domain_range(file_name)
   # file_name = 'edge_domain_range.csv'
   # get_edge_domain_range(file_name)
   # file_name = 'entity_domain_range.txt'
   # the connection to neo4j
   HOST = 'localhost'
   PORT = 7687
   USER = 'neo4j'
   PASS = 'password'
   GRAPH = Graph(host=HOST, port=PORT, user=USER, password=PASS)
   file_name = 'refined_domain_range_2.csv'
   get_refined_domain_range_2(file_name)