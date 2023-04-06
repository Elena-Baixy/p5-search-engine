#!/usr/bin/env python3
"""Reduce 0.


Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools
from collections import Counter



def reduce_one_group(key, group):
    group = list(group)
    for line in group:
        # print(line)
        docid, term, idf, tf, normalization_factor = line.split()
        # print(term)
        print(f"{term} {idf} {docid} {tf} {normalization_factor}")
    return 0


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    #group by doc_i
    
    # term_idf_tf_norm = line.partition("\t")[2].strip()
    # term = term_idf_tf_norm.split()[0]
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    count = 0
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)
    # print(count)


if __name__ == "__main__":
    main()