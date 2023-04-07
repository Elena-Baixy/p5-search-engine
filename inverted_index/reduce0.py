#!/usr/bin/env python3
"""Reduce 0.

Template reducer.
 output doc_id % 3 as the key in the last map stage, and output normally to standard output in the last reduce stage. 

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools


def reduce_one_group(line):
    """Reduce one group."""
    print(line)


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for line in sys.stdin:
        reduce_one_group(line)
        #where can I get those data


if __name__ == "__main__":
    main()