#!/usr/bin/env python3

"""Map 0."""
import csv
import sys
import re
from collections import Counter

csv.field_size_limit(sys.maxsize)


def clean():
    """Clean the data. return tuple_word[[]] as (doc_id,term)."""
    tokens = []
    filtered_sentence = []
    tuple_word = []
    stopwords_list = []
    with open("stopwords.txt", "r", encoding="utf-8") as stopwords:
        for line in stopwords:
            line = line.replace("\n", "")
            stopwords_list.append(line)

    #     csv_reader = csv.reader(file)
    csv_reader = csv.reader(sys.stdin)
    for row in csv_reader:
        if len(row) != 0:
            new_row = row[1] + " " + row[2]
            new_row = re.sub(r"[^a-zA-Z0-9 ]+", "", new_row)
            new_row = new_row.replace("  ", " ")
            new_row = new_row.casefold()
            new_row = new_row.strip()
            tokens = new_row.split(" ")
            for token in tokens:
                if token not in stopwords_list:
                    filtered_sentence.append((row[0], token))
            tuple_word.append(filtered_sentence)
            filtered_sentence = []
    return tuple_word


def bound(tuple_word):
    """Return{doc_id} {term} t {t_f}."""
    id_word = {}
    for doc in tuple_word:
        new_dict = dict(Counter(doc))
        id_word.update(new_dict)
    # pprint(id_word)
    for (docid, term), t_f in id_word.items():
        print(f"{docid} {term}\t{t_f}")


tupled_word = clean()
bound(tupled_word)
