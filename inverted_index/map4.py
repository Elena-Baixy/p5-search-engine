#!/usr/bin/env python3
"""Map 0."""
import csv
import sys

csv.field_size_limit(sys.maxsize)


# {term},{idf} \t {docid} {tf} {normalization_factor} -> {docid} {tf} {di}
for line in sys.stdin:
    line = line.replace("\t"," ").replace("\n","")
    term = line.split(",",1)[0]
    idf_dc_tf_nrom = line.split(",",1)[1]
    print(f"{term}\t{idf_dc_tf_nrom}")
