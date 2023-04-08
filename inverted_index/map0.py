#!/usr/bin/env python3

"""Map 0."""
import csv
import sys
import re
from collections import Counter
from pprint import pprint

csv.field_size_limit(sys.maxsize)

def count():
    '''Job 0, calculate N.'''
    csv_reader = csv.reader(sys.stdin)
    rows = list(csv_reader)
    length = len(rows)
    print(f"{1} \t {length}")
    # 直接print就行 reduce stage 会read stdin，pipeline.sh会帮print的搬到output dir去

    # with open('output0/total_document_count.txt', 'w') as output_file:
    #     output_file.write(str(length))
    return 0

count_num = count()

