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
    with open('example_input/input.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        rows = list(csv_reader)
        length = len(rows)
        print(length)
    # with open('output0/total_document_count.txt', 'w') as output_file:
    #     output_file.write(str(length))
    return 0

count_num = count()

