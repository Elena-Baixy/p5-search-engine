#!/usr/bin/env python3
"""Reduce 0.


Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools
from collections import Counter


def order(key, group,combined):
    group = list(group)
    for line in group:
        line = line.replace("\n","")
        #line = line.replace("\t ","")
        key = line.split("\t")[0]
        line = line.split("\t")[1]
        term = line.split(" ",1)[0]
        value = line.split(" ",2)[2]
        term_pair = key + " " + term
        if term_pair not in combined:
            combined[term_pair] = line
        else:
            combined[term_pair] = combined[term_pair] + " " + value
        # print(term_pair + " " + combined[term_pair] + " " +value)

def reduce_one_group(key,group):
    group = list(group)
    for line in group:
        line = line.replace("\n",'')
        ouputval = line.split("\t")[1]
        print(f"{ouputval}")
    # for term_pair in combined:
    #     print(f"{combined[term_pair]}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    #combined = {}
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        #order(key, group,combined)
        reduce_one_group(key, group)
    # print(count)


if __name__ == "__main__":
    main()