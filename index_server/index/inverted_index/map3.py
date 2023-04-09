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
    docid = line.split()[0]
    term = line.split()[1]
    tf = line.split()[2]
    idf = line.split()[3]
    w_square = line.split()[4]
    print (f"{docid} \t {term} {tf} {idf} {w_square}")
    # words = line.split()
    # print (words)
    # for word in words:
    #     print(f"{word}\t")
