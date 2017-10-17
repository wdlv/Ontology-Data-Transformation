## Ontology_Data_Transformation

# Environment Requirement:
Python 3.6<br/>  pandas<br/>  sqlite3<br/> nltk<br/>  rdflib

# Introduction

1. rdf2csv.py

This script is to transform rdf,xrdf format data into csv and print out all the unique predicates along with their examples. In general, different ontology might use different predicates to represent the same relationship. So it is quite important for us to find out corresponding predicates for our desired ontology. Predicate examples could be found in the Radiology Lexicon Predicates and Examples.txt

2. csv2sqlDB.py

This script is to transform triples following the standard of SKOS(The Simple Knowledge Organization System) and store graph info into a sql database. The script is initially intended to work on BioPortal's Radiology Lexicon(https://bioportal.bioontology.org/ontologies/RADLEX). However, these codes could be easily adapted to work on other ontology.

SQL Database here has three tables - Concept, Broaders, Related.

Concept table has 6 attributes - ConceptURI, PrefLabel, AltLabel, ScopeNotes, TopConcept, NormPrefLabel

# One Radiology example in the Concept table:

http://www.radlex.org/RID/#RID3441<br/>
reflux esophagitis<br/>
Refluxösophagitis<br/>
inflammation of the esophagus that is caused by the reflux of gastric juice with contents of the stomach and duodenum. [MeSH]<br/>
RID0<br/>
reflux esophag


