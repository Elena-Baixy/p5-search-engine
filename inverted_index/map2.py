#!/usr/bin/env python3
"""Map 0."""
import csv
import sys
import re
from collections import Counter
from pprint import pprint

csv.field_size_limit(sys.maxsize)

import sys

with open('total_document_count.txt', 'r') as file:
    N = file.readline().strip()

for line in sys.stdin:
    term = line.split()[1]
    docid = line.split()[0]
    tf = line.split()[2]
    #N = line.split()[3]
    # N = 3268
    # print(N)
    print (f"{term}\t{docid} {tf} {N}")


