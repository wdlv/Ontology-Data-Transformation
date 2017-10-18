#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 15:22:42 2017

@author: Hongwei Liu
"""

import sqlite3
import os
import pandas as pd
from nltk.stem.porter import PorterStemmer

db = None
stop = set()
stemmer = PorterStemmer()

broader_pred = "http://www.w3.org/2000/01/rdf-schema#subClassOf"
prefer_pred = "http://www.radlex.org/RID/#Preferred_name"
related_pred = "http://www.radlex.org/RID/#Related_modality"
alt_pred = "http://www.radlex.org/RID/#Synonym"
note_pred = "http://www.radlex.org/RID/#Definition"
thing = "http://www.w3.org/2002/07/owl#Thing"


def main(dbname):
    db_create(dbname)
    db_connect(dbname)
    get_top_concepts()
    getCoreConcepts()
    getBroaders()
    getRelated()
    db.commit()
    db.close()

def get_word(URI):
    return URI.split('#')[-1]


def start(file):
    global datafile
    datafile = pd.read_csv(file)

def get_top_concepts():

    target_pred = broader_pred
    target_obj_word = thing
    # Find all the triples whose object is 'Thing' and get their subject - Top Concept.
    topconceptlist = []

    for _ , value in datafile[datafile['object'] == target_obj_word].iterrows():
        topconceptlist.append(get_word(value['subject']))

    # Create top concepts dictionary
    global topconceptTree
    topconceptTree = {}

    for x in topconceptlist:
        topconceptTree[x] = [x]
    print('The top concepts in this ontology are:', topconceptlist)

    # Get all the nodes having narrower or broader predicate and generate a list to store qualified subject and object(not blank node) information.
    relationlist = []
    print('Now the program is creating a list to collect all the (subject, object) tuples...')

    for _, value in datafile[datafile['predicate'] == target_pred].iterrows():
        if get_word(value['object']) != target_obj_word:
            relationlist.append((get_word(value['subject']), get_word(value['object'])))

            if len(relationlist) % 100 == 0:
                print('{:d} tuples have been collected.'.format(len(relationlist)))

    print('Tuples collection finished.')
    print('Now the program is creating the tree...')

    tupleNum = len(relationlist)
    topNum = len(topconceptlist)
    # Generate all the following nodes for each top concepts.
    while len(relationlist) > topNum:
        for tup in relationlist:
            for key, value in topconceptTree.items():
                if tup[1] in value:
                    topconceptTree[key].append(tup[0])
                    relationlist.remove(tup)
                    if (len(relationlist) - topNum) % 100 == 0:
                        print('Tree constructing completed {:.2%}'.format(1 - (len(relationlist) - topNum)/(tupleNum - topNum)))

    print('Tree construction finished.\n')

def getCoreConcepts():
    # Get all the concepts
    target_pred = prefer_pred
    target_obj_word = thing
    conceptlist = []

    for _, value in datafile[datafile['predicate'] == target_pred].iterrows():
        if value['subject'] != target_obj_word:
            conceptlist.append((value['subject'], value['object']))
    
    for x in conceptlist:
        obj = x[0]
        prefLabel = get_word(x[1])
        altLabel = getAltLabel(obj)
        scopeNotes = getScopeNotes(obj)

        topConcept = ''

        for key, value in topconceptTree.items():
            if get_word(obj) in value:
                topConcept = key
                break

        addConcept(obj, prefLabel, altLabel, scopeNotes, topConcept)
        print('\n'.join([obj, prefLabel, altLabel, scopeNotes, topConcept, '']))

def getBroaders():
    target_pred = broader_pred
    for _, value in datafile[datafile['predicate'] == target_pred].iterrows():
        addBroader(get_word(value['subject']), get_word(value['object']))
        

def getRelated():
    pass
    target_pred = related_pred
    for _, value in datafile[datafile['predicate'] == target_pred].iterrows():
        addRelated(get_word(value['subject']), get_word(value['object']))

def getAltLabel(obj):
    target_pred = alt_pred
    word_return = ''
    for _, value in datafile[datafile['predicate'] == target_pred].iterrows():
        if get_word(value['subject']) == obj.split('#')[1]:
            word_return = get_word(value['object'])
    return word_return

def getScopeNotes(obj):
    target_pred = note_pred
    word_return = "This concept does not have scope notes."
    for _, value in datafile[datafile['predicate'] == target_pred].iterrows():
        if get_word(value['subject']) == obj.split('#')[1]:
            word_return = get_word(value['object'])
    return word_return

def addConcept(conceptURI, prefLabel, altLabel, scopeNotes, topConcept):
    global db
    try:
        normPrefLabel = normalize(prefLabel)
        cursor = db.cursor()
        cursor.execute("INSERT INTO CONCEPT (ConceptURI, PrefLabel, AltLabel, ScopeNotes, TopConcept, NormPrefLabel) VALUES (?,?,?,?,?,?)",(conceptURI, prefLabel, altLabel, scopeNotes, topConcept, normPrefLabel))
    except sqlite3.IntegrityError as err:
        print('Integrity Error on addConcept:', err)
    except sqlite3.OperationalError as err:
        print('Operational Error on addConcept:', err)
    except sqlite3.Error as err:
        print('Error on connect:', err)

def addBroader(subjectURI, objectURI):
    global db
    try:
        cursor = db.cursor()
        cursor.execute("INSERT INTO BROADERS (ConceptURI, BroaderThanURI) VALUES (?,?)",(objectURI, subjectURI))
    except sqlite3.IntegrityError as err:
        print('Integrity Error on addBroader:', err)
    except sqlite3.OperationalError as err:
        print('Operational Error on addBroader:', err)
    except sqlite3.Error as err:
        print('Error on connect:', err)


def addRelated(subjectURI, objectURI):
    global db
    try:
        cursor = db.cursor()
        cursor.execute("INSERT INTO RELATED (ConceptURI, RelatedURI) VALUES (?,?)",(subjectURI, objectURI))
    except sqlite3.IntegrityError as err:
        print('Integrity Error on addRelated:', err)
    except sqlite3.OperationalError as err:
        print('Operational Error on addRelated:', err)
    except sqlite3.Error as err:
        print('Error on connect:', err)


def createStopwordsList():
    global stop
    stop_word_file = "SmartStoplist.txt"
    stop_words = []
    for line in open(stop_word_file):
        if line.strip()[0:1] != "#":
            for word in line.split():  # in case more than one per line
                stop_words.append(word)
    stop = set(stop_words)


def normalize(prefLabel):
    global stop
    prefLabel = prefLabel.lower()
    prefList = prefLabel.split(" ")
    stopfree_words = [word for word in prefList if word not in stop]
    stoppedAndStemmed = stemList(stopfree_words)
    space = ' '
    normPrefLabel = space.join(stoppedAndStemmed)
    return normPrefLabel


def stemList(wordList):
    stemmed = []
    for word in wordList:
        stemmedword = stemmer.stem(word)
        stemmed.append(stemmedword)
    return stemmed


def db_create(dbname):
    try:
        db = sqlite3.connect(dbname)
        c = db.cursor()
        # Drop existing desired table
        c.execute('''DROP TABLE IF EXISTS "BROADERS";''')
        c.execute('''DROP TABLE IF EXISTS "RELATED";''')
        c.execute('''DROP TABLE IF EXISTS "CONCEPT";''')
        
        # Create table
        c.execute('''CREATE TABLE CONCEPT
                  (ConceptURI    VARCHAR(100)   NOT NULL,
                  PrefLabel      VARCHAR(100)   NOT NULL,
                  AltLabel       VARCHAR(100),
                  ScopeNotes    VARCHAR(500),
                  TopConcept    INTEGER DEFAULT '0',
                  NormPrefLabel VARCHAR NOT NULL,
                  PRIMARY KEY (ConceptURI));''')
        
        c.execute('''CREATE TABLE BROADERS
                  (ConceptURI        VARCHAR(100)   NOT NULL,
                  BroaderThanURI    VARCHAR(100)   NOT NULL,
                  PRIMARY KEY (ConceptURI, BroaderThanURI),
                  FOREIGN KEY (ConceptURI) REFERENCES CONCEPT(ConceptURI),
                  FOREIGN KEY (BroaderThanURI) REFERENCES CONCEPT(ConceptURI));''')
        
        c.execute('''CREATE TABLE RELATED
                  (ConceptURI     VARCHAR(100)   NOT NULL,
                  RelatedURI     VARCHAR(100)   NOT NULL,
                  PRIMARY KEY (ConceptURI, RelatedURI),
                  FOREIGN KEY (ConceptURI) REFERENCES CONCEPT(ConceptURI),
                  FOREIGN KEY (RelatedURI) REFERENCES CONCEPT(ConceptURI));''')
        
        # Save (commit) the changes and close database
        db.commit()
        db.close()
        
    except:
        print('Error:', dbname, 'does not exist')


def db_connect(dbname):
    global db
    try:
        if os.path.exists(dbname):
            db = sqlite3.connect(dbname)
        else:
            print('Error:', dbname, 'does not exist')
    except sqlite3.IntegrityError as err:
        print('Integrity Error on connect:', err)
    except sqlite3.OperationalError as err:
        print('Operational Error on connect:', err)
    except sqlite3.Error as err:
        print('Error on connect:', err)

if __name__ == '__main__':
    start('radio63.csv')
    main('example.db')
