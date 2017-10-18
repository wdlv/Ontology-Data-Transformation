#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 15:22:42 2017

@author: Hongwei Liu
"""

import rdflib
import os
import pandas as pd
import time

def rdf2csv(filename, outputname):
    startTime = time.time()
    g = rdflib.Graph()
    result = g.parse(filename)
    print("graph has %s statements." % len(g))

    # a list to collect s, p, o
    collect_list = []
    # process indicator
    total = len(result)
    n = 0.0

    # Iterate rdf document
    for s, p, o in g:
        n += 1

        # Print every 100 triples
        if n % 100 == 0:
            print("Percentage: {:.2%}".format(n/total))

        # Turn URI format to bytes to str
        s = s.encode('utf-8').decode("utf-8")
        p = p.encode('utf-8').decode("utf-8")
        o = o.encode('utf-8').decode("utf-8")

        # Avoid all the blank nodes
        if s[:1] != "N" and o[:1] != "N":
            collect_list.append((s, p, o))

    # Create a global dataframe to hold data
    global df
    df = pd.DataFrame(collect_list, columns=['subject', 'predicate', 'object'])

    df.to_csv(outputname + '.csv', index = False)

    endTime = time.time()

    print("Transformation has used {:.2f} seconds".format(endTime - startTime))
    print('***Finished***\n')

def get_word(URI):
    # Get exact word from website-like link
    return URI.split('#')[-1]

def displaySPOexample(exampleNum):
    # Get all the unique predicates
    predicate_list = set(df['predicate'])

    for one in predicate_list:
        counter = 0
        rdfexample = []

        for _ , value in df[df['predicate'] == one].iterrows():
            # For each predicate find a number of examples
            tup = (get_word(value['subject']), value['predicate'], get_word(value['object']))
            rdfexample.append(tup)

            counter += 1
            if counter == exampleNum:
                print('Triple Example:', one)
                for temp in rdfexample:
                    print(temp)
                print('***' * 6)
                break


if __name__ == '__main__':
    rdf2csv("Radiology Lexicon.xrdf", 'radio63')
    displaySPOexample(3)


