# Ontology Data Transformation

## Environment:
Python 3.6

pandas

sqlite3

nltk

rdflib

## Introduction

### 1. rdf2csv.py

This script is to transform rdf, xrdf format data into csv and print out all the unique predicates along with their examples. In general, different ontology might use different predicates to represent the same relationship. So it is quite important for people to map new predicates in a new ontology to their target ontology.

### 2. csv2sqlDB.py

This script is to transform triples following the standard of SKOS(The Simple Knowledge Organization System) and store graph info into a sql database. The script is initially intended to work on BioPortal's Radiology Lexicon(https://bioportal.bioontology.org/ontologies/RADLEX). However, these codes could be easily adapted to work on other ontology.

### 3. Database Info:

SQL Database here has three tables - Concept, Broaders, Related.

The Concept table has 6 attributes - ConceptURI, PrefLabel, AltLabel, ScopeNotes, TopConcept, NormPrefLabel

### 4. Radiology Lexicon Predicates and Examples.txt:

Predicates and their examples that the rddf2csv.py script extracted from a new ontology. People could quickly identify which predicates are their desired predicates based on those examples.

***
## One Radiology example in the Concept table:
```
Subject : http://www.radlex.org/RID/#RID3441
```
### Original:

|Predicate|Object|
|---|---
|http://www.radlex.org/RID/#Preferred_name|reflux esophagitis
|http://www.w3.org/2000/01/rdf-schema#subClassOf|http://www.radlex.org/RID/#RID3440
|http://www.w3.org/1999/02/22-rdf-syntax-ns#type|http://www.w3.org/2002/07/owl#NamedIndividual
|http://www.radlex.org/RID/#Is_A|http://www.radlex.org/RID/#RID3440
|http://data.bioontology.org/metadata/prefixIRI|RID3441
|http://www.w3.org/1999/02/22-rdf-syntax-ns#type|http://www.radlex.org/RID/#pathophysiology_metaclass
|http://www.w3.org/2000/01/rdf-schema#label|RID3441
|http://www.radlex.org/RID/#Synonym|Refluxösophagitis
|http://www.radlex.org/RID/#UMLS_Term|reflux esophagitis
|http://www.radlex.org/RID/#UMLS_ID|C0014869
|http://www.radlex.org/RID/#Definition|inflammation of the esophagus that is caused by the reflux of gastric juice with contents of the stomach and duodenum. [MeSH]
|http://www.w3.org/1999/02/22-rdf-syntax-ns#type|http://www.w3.org/2002/07/owl#Class


### Transformed:

|Concept Table| |
|---|---
ConceptURI|http://www.radlex.org/RID/#RID3441
PrefLabel|reflux esophagitis
AltLabel|Refluxösophagitis
ScopeNotes|inflammation of the esophagus that is caused by the reflux of gastric juice with contents of the stomach and duodenum. [MeSH]
TopConcept|RID0
NormPrefLabel|reflux esophag


