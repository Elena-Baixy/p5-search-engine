#!/usr/bin/env python3
"""Map 0."""
import csv
import sys
import re
from collections import Counter
from pprint import pprint

csv.field_size_limit(sys.maxsize)

import sys

for line in sys.stdin:
    term = line.split()[1]
    docid = line.split()[0]
    tf = line.split()[2]
    N = line.split()[3]
    print (f"{term} \t {docid} {tf} {N}")
    # words = line.split()
    # print (words)
    # for word in words:
    #     print(f"{word}\t")



def clean():
    '''cleaning the data. return tuple_word[[]] as (doc_id,term).'''
    tokens = []
    filtered_sentence = []
    tuple_word = []
    stopwords_list =[]
    with open("stopwords.txt", "r") as stopwords:
        for line in stopwords:
            line = line.replace("\n","")
            stopwords_list.append(line)
    with open('example_input/input.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            new_row = row[1] + " " + row[2]
            new_row = re.sub(r"[^a-zA-Z0-9 ]+", "", new_row)
            new_row = new_row.replace("  "," ")
            new_row = new_row.casefold()
            tokens = new_row.split(" ")
            for token in tokens:
                if token not in stopwords_list:
                    filtered_sentence.append((row[0],token))
            tuple_word.append(filtered_sentence)
            filtered_sentence = []
    val = 1
    for doc in tuple_word:
        for tup in doc:
            # print(tup)
            print (f"{tup}\t{val}")
    return tuple_word


def bound(tuple_word): 
    '''Count_tf,return a ((doc_id,term),tf) dict.'''
    id_word = {}
    for doc in tuple_word:
        # pprint(doc)
        new_dict = dict(Counter(doc))
        # pprint(new_dict)
        id_word.update(new_dict)
    # for key,value in id_word.items():
    #     print(f"{key[0]}\t{key[1]}\t{value}")
        # pprint(id_word)
    return id_word

def count_nk(id_word):
    '''Count_nk.'''
    word_value = []
    for key,value in id_word:
        word_value.append(value)
    for word in word_value:
        word_nk = dict(Counter(word_value))
    print(word_nk)
    # breakpoint()


#count()
# tuple_word = clean()
# id_word = bound(tuple_word)
# count_nk(id_word)
