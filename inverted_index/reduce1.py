#!/usr/bin/env python3
"""Reduce 0.

Template reducer.
 output doc_id % 3 as the key in the last map stage, and output normally to standard output in the last reduce stage. 

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools
from collections import Counter
from pprint import pprint


def reduce_one_group(line,word_value):
    """Reduce one group."""
    #print(line)
    #line = line.split(" ")
    line = line.replace("\n",'')
    line = line.replace(", ",',')
    word_value[line.split(" ")[0]] = line.split(" ")[1]
    #pprint(word_value)
    return word_value
    
def count_nk(word_value):
    for word in word_value:
        word_nk = dict(Counter(word_value))
    #pprint(word_nk)
    #breakpoint()


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    word_value = {}
    for line in sys.stdin:
        reduce_one_group(line,word_value)
        #breakpoint()
    count_nk(word_value)
    pprint(word_value)


if __name__ == "__main__":
    main()