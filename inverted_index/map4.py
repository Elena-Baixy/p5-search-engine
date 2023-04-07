#!/usr/bin/env python3
"""Map 0."""
import csv
import sys
import re
from collections import Counter
from pprint import pprint

csv.field_size_limit(sys.maxsize)

import sys

# {term} {docid} \t {idf} {tf} {normalization_factor} -> {docid} {tf} {di}
combined = {}
for line in sys.stdin:
    line = line.replace(" \t ",",")
    termid,value = line.split(",")
    value = value.replace("\n","")
    idf = (value.split(" ",1))[0]
    value = (value.split(" ",1))[1]
    docid = (termid.split(" ",1))[1]
    key = int(docid) % 3
    term = (termid.split(" ",1))[0]
    term = term + " " + str(key)
    #term = (termid.split(" ",1))[0]
    #如果%3一样则要放在同一行，而不是docid一样
    value = idf + " " + docid + " " + value
    if term not in combined:
        combined[term] = value
    else:
        value = (value.split(" ",1))[1]
        combined[term] = combined[term] + " " +value
# {term} {idf} : {docid} {tf} {di}

for termid in combined:
    term = (termid.split(" ",1))[0]
    idf =  (combined[termid].split(" ",1))[0]
    term = term + " " + idf
    value = (combined[termid].split(" ",1))[1]
    docid = (value.split(" ",1))[0]
    key = int(docid) % 3
    print(f"{key} \t {term} {value}")

    #key = int(line.split()[2]) % 3
    
    # print(key)
    #print (f"{key} \t {line.split()[0]}  {line.split()[1]} {line.split()[3]} {line.split()[4]} {line.split()[2]}")
