#!/usr/bin/env python3
"""Reduce 0.


Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools
import math
from collections import Counter



def reduce_one_group(key, group):
    group = list(group)

    # calculate x_mean or y_mean
    normalization_factor = 0
    for line in group:
        docid, term, tf,idf, w_squared = line.split()
        w_squared = float(w_squared)
        normalization_factor += w_squared
    # normalization_factor = math.sqrt(normalization_factor)

    for line in group:
        docid, term, tf,idf, w_squared = line.split()
        print(f"{term} {docid} \t {idf} {tf} {normalization_factor}")
    return 0


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    #group by doc_id
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    count = 0
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(key, group)
    # print(count)


if __name__ == "__main__":
    main()