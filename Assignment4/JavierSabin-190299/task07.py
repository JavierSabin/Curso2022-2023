# -*- coding: utf-8 -*-
"""Task07.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tV5j-DRcpPtoJGoMj8v2DSqR_9wyXeiE

**Task 07: Querying RDF(s)**
"""

#!pip install rdflib 
github_storage = "https://raw.githubusercontent.com/FacultadInformatica-LinkedData/Curso2020-2021/master/Assignment4"

"""Leemos el fichero RDF de la forma que lo hemos venido haciendo"""

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS
g = Graph()
g.namespace_manager.bind('ns', Namespace("http://somewhere#"), override=False)
g.namespace_manager.bind('vcard', Namespace("http://www.w3.org/2001/vcard-rdf/3.0#"), override=False)
g.parse(github_storage+"/resources/example6.rdf", format="xml")

"""TASK 7.1: List all subclasses of "Person" with RDFLib and SPARQL"""
# RDF
ns = Namespace("http://somewhere#")
for s,p,o in g.triples((None, RDFS.subClassOf, ns.Person)):
  print(s)
  
# SPARQL
from rdflib.plugins.sparql import prepareQuery
query = prepareQuery('''
  SELECT DISTINCT ?subClass
  WHERE{
	  ?subClass (rdfs:subClassOf/rdfs:subClassOf*) ns:Person		     
  }							                                            
  ''',
  initNs = {"rdfs": RDFS, "ns": ns}
)
for i in g.query(query):
  print(i)

"""TASK 7.2: List all individuals of "Person" with RDFLib and SPARQL (remember the subClasses)""""
# RDF
for s, p, o in g.triples((None, RDF.type, ns.Person)):
  print(s)
for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
  for s2, p2, o2 in g.triples((None, RDF.type, s)):
    print(s2)


# SPARQL
query2 = prepareQuery('''
  SELECT DISTINCT ?Person
  WHERE{
    {?Person rdf:type ns:Person} UNION
	  {?Person2 rdfs:subClassOf/rdfs:subClassOf* ns:Person .
    ?Person rdf:type ?Person2
    } 
  }
  ''',
  initNs = {"rdf": RDF, "rdfs": RDFS, "ns": ns}
)
for j in g.query(query2):
  print(j)

"""TASK 7.3: List all individuals of "Person" and all their properties including their class with RDFLib and SPARQL"""
# RDF
for s, p, o in g.triples((None, RDF.type, ns.Person)):
  for s2, p2, o2 in g.triples((s, None, None)):
    print(s2, p2, o2)
for s, p, o in g.triples((None, RDFS.subClassOf, ns.Person)):
  for s2, p2, o2 in g.triples((None, RDF.type, s)):
    for s3, p3, o3 in g.triples((s2, None, None)):
      print(s3, p3, o3)


# SPARQL
query3 = prepareQuery('''
  SELECT DISTINCT ?Person ?Property ?Object
  WHERE{
  	{
    ?Person rdf:type ?Person2 .
    ?Person2 (rdfs:subClassOf/rdfs:subClassOf*) ns:Person .
    ?Person ?Property ?Object
    } UNION {
    ?Person rdf:type ns:Person .
    ?Person ?Property ?Object
    }
  }
  ''',
  initNs = {"rdf": RDF, "rdfs": RDFS, "ns": ns}
)
for k in g.query(query3):
  print(k)