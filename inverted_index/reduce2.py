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
    count = 0
    nk = len(group)
    for line in group:
        line = line.replace("\t"," ")
        term = line.split(" ")[0]
        docid = line.split(" ")[1]
        tf = line.split(" ")[2]
        N = line.split(" ")[3]
        N = int(N)
        tf = int (tf)
        # idf  = math.log10(N/nk)
        # w = tf * idf
        # w_squared = w * w
        print(f"{docid}\t{term} {tf} {nk} {N} ")
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