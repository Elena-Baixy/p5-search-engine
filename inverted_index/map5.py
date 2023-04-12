#!/usr/bin/env python3

"""Map 0."""
import csv
import sys

csv.field_size_limit(sys.maxsize)


# {term} {idf} \t {docid} {tf} {normalization_factor} -> {docid} {tf} {di}
for line in sys.stdin:
    line = line.replace("\t", " ").replace("\n", "")
    term = line.split(" ", 1)[0]
    line = line.split(" ", 1)[1]
    idf = line.split(" ", 1)[0]
    doc_tf_norm = line.split(" ", 1)[1]
    doc_tf_norm = doc_tf_norm.split(" ")
    PART0 = ""
    PART1 = ""
    PART2 = ""
    for i in range(1, len(doc_tf_norm), 3):
        if int(doc_tf_norm[i]) % 3 == 0:  # docid
            PART0 = (
                PART0
                + " "
                + doc_tf_norm[i]
                + " "
                + doc_tf_norm[i + 1]
                + " "
                + doc_tf_norm[i + 2]
            )
        elif int(doc_tf_norm[i]) % 3 == 1:
            PART1 = (
                PART1
                + " "
                + doc_tf_norm[i]
                + " "
                + doc_tf_norm[i + 1]
                + " "
                + doc_tf_norm[i + 2]
            )
        elif int(doc_tf_norm[i]) % 3 == 2:
            PART2 = (
                PART2
                + " "
                + doc_tf_norm[i]
                + " "
                + doc_tf_norm[i + 1]
                + " "
                + doc_tf_norm[i + 2]
            )
    if PART0 != "":
        print(f"0\t{term} {idf} {PART0.rstrip(' ')}")
    if PART1 != "":
        print(f"1\t{term} {idf} {PART1.rstrip(' ')}")
    if PART2 != "":
        print(f"2\t{term} {idf} {PART2.rstrip(' ')}")
