#!/usr/bin/env python3
"""Map 0."""
import csv
import sys
import re
import os
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

    # with open("../tests/testdata/test_pipeline14/input_multi/input1.csv","r") as file:
    #     csv_reader = csv.reader(file)
    csv_reader = csv.reader(sys.stdin)
    for row in csv_reader:
        if len(row) != 0:
            new_row = row[1] + " " + row[2]
            new_row = re.sub(r"[^a-zA-Z0-9 ]+", "", new_row)
            new_row = new_row.replace("  "," ")
            new_row = new_row.casefold()
            new_row = new_row.strip()
            tokens = new_row.split(" ")
            for token in tokens:
                if token not in stopwords_list:
                    filtered_sentence.append((row[0],token))
            tuple_word.append(filtered_sentence)
            filtered_sentence = []
    return tuple_word


def bound(tuple_word): 
    '''Return{doc_id} {term} t {tf}.'''
    #with open('total_document_count.txt', 'r') as file:
    #    total_docu_count = file.readline().strip()
    id_word = {}
    for doc in tuple_word:
        new_dict = dict(Counter(doc))
        id_word.update(new_dict)
    #pprint(id_word)
    for (docid,term),tf in id_word.items():
        print(f"{docid} {term}\t{tf}")

tuple_word = clean()
bound(tuple_word)
# def clean():
# tokens = []
# filtered_sentence = []
# tuple_word = []
# stopwords_list =[]
# total_docu_count = 0 
# with open("stopwords.txt", "r") as stopwords:
#     for line in stopwords:
#         line = line.replace("\n","")
#         stopwords_list.append(line)


# with open('example_input/input.csv', 'r') as csv_file:
#     csv_reader = csv.reader(csv_file)

#     for row in csv_reader:
#         new_row = row[1] + " " + row[2]
#         new_row = re.sub(r"[^a-zA-Z0-9 ]+", "", new_row)
#         new_row = new_row.replace("  "," ")
#         new_row = new_row.casefold()
#         tokens = new_row.split(" ")
#         for token in tokens:
#             if token not in stopwords_list:
#                 docid = row[0]
#                 print (f"{docid} {token}\t {total_docu_count}")


