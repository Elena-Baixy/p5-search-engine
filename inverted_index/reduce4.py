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

    # calculate x_mean or y_mean
    tf_list = []
    # print(key)
    tf_list.append(key)
    for line in group:
        docid_tf_norm = line.split("\t")[1].strip()
        tf_list.append(docid_tf_norm)
    print(tf_list)
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