#!/usr/bin/env python3
"""Map 3."""
import csv
import sys
import re
import math
from collections import Counter
from pprint import pprint

csv.field_size_limit(sys.maxsize)

import sys

with open('total_document_count.txt', 'r') as file:
    N = file.readline().strip()

for line in sys.stdin:
    docid = line.split("\t")[0]
    line = line.split("\t")[1]
    term = line.split()[0]
    nk = line.split()[2]
    tf = line.split()[1]
    print (f"{docid}\t{term} {tf} {nk} {N}")