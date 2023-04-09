#!/usr/bin/env python3
"""Map 0."""
import csv
import sys
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
    total_docu_count = 0 
    with open("stopwords.txt", "r") as stopwords:
        for line in stopwords:
            line = line.replace("\n","")
            stopwords_list.append(line)
    with open('total_document_count.txt', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        rows = list(csv_reader)
        total_docu_count = int (rows[0][0])
        # print(total_docu_count)

    with open('example_input/input.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)  
        # print(total_docu_count)
        # csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            # total_docu_count +=1
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
            print (f"{tup}\t {total_docu_count}")
    return tuple_word


#count()
tuple_word = clean()

