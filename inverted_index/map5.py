#!/usr/bin/env python3
"""Map 0."""
import csv
import sys
import re
from collections import Counter
from pprint import pprint

csv.field_size_limit(sys.maxsize)

import sys


# {term} {idf} \t {docid} {tf} {normalization_factor} -> {docid} {tf} {di}
for line in sys.stdin:
    line = line.replace("\t"," ").replace("\n","")
    term = line.split(" ",1)[0]
    line = line.split(" ",1)[1]
    idf = line.split(" ",1)[0]
    doc_tf_norm = line.split(" ",1)[1]
    doc_tf_norm = doc_tf_norm.split(" ")
    part0 = ''
    part1 = ''
    part2 = ''
    for i in range (1,len(doc_tf_norm),3):
        if int(doc_tf_norm[i]) % 3 == 0: #docid
            part0 = part0 + " " + doc_tf_norm[i] + " " + doc_tf_norm[i+1] + " " + doc_tf_norm[i+2]
        elif int(doc_tf_norm[i]) % 3 == 1:
            part1 = part1 + " " + doc_tf_norm[i] + " " + doc_tf_norm[i+1] + " " + doc_tf_norm[i+2]
        elif int(doc_tf_norm[i]) % 3 == 2:
            part2 = part2 + " " + doc_tf_norm[i] + " " + doc_tf_norm[i+1] + " " + doc_tf_norm[i+2]
    if part0 != '':
        print(f"0\t{term} {idf} {part0.rstrip(' ')}")
    if part1 != '':
        print(f"1\t{term} {idf} {part1.rstrip(' ')}")
    if part2 != '':
        print(f"2\t{term} {idf} {part2.rstrip(' ')}")