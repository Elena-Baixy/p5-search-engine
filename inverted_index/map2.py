#!/usr/bin/env python3

"""Map 0."""
import csv
import sys

csv.field_size_limit(sys.maxsize)


with open("total_document_count.txt", "r", encoding="utf-8") as file:
    N = file.readline().strip()

for line in sys.stdin:
    line = line.replace("\t", " ")
    term = line.split(" ")[1]
    docid = line.split(" ")[0]
    tf = line.split(" ")[2]
    # N = line.split()[3]
    # N = 3268
    # print(N)
    print(f"{term}\t{docid} {tf} {N}")
