#!/usr/bin/env python3
import sys
import csv
import re
from collections import Counter
from pprint import pprint


csv.field_size_limit(sys.maxsize)
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
    return tuple_word


def bound(tuple_word): 
    '''Count_tf,return a ((doc_id,term),tf) dict.'''
    id_word = {}
    for doc in tuple_word:
        new_dict = dict(Counter(doc))
        id_word.update(new_dict)
    #pprint(id_word)
    for line,value in id_word.items():
        print(line,value)

def count_nk(id_word):
    '''Count_nk.'''
    word_value = []
    for key,value in id_word:
        word_value.append(value)
    for word in word_value:
        word_nk = dict(Counter(word_value))
    #pprint(word_nk)
    breakpoint()

tuple_word = clean()
#pprint(tuple_word)
bound(tuple_word)
#count_nk(id_word)