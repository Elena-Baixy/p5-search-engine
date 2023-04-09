#!/usr/bin/env python3
"""Reduce 0.

Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools


def reduce_one_group(key, group):
    group = list(group)

    # calculate x_mean or y_mean
    for line in group:
        print(line)

    return 0


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    #group by doc_id
    # print(line)
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    count = 0
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        # count +=1
        reduce_one_group(key, group)
    # print(count)


if __name__ == "__main__":
    main()
