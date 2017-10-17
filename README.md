## Ontology_Data_Transformation

# Environment Requirement:
Python 3.6
pandas
sqlite3
nltk
rdflib

# Introduction

1. rdf2csv.py
This script is to transform rdf,xrdf format data into csv and print out all the unique predicates along with their examples. In general, different ontology might use different predicates to represent the same relationship. So it is quite important for us to find out corresponding predicates to desired ontology.

2. csv2sqlDB.py
This script is to transform triples following the standard of SKOS(The Simple Knowledge Organization System) and store graph info into a sql database. The script is initially intended to work on BioPortal's Radiology Lexicon(https://bioportal.bioontology.org/ontologies/RADLEX). However, these codes could be easily adapted to work on other ontology.




