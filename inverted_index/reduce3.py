#!/usr/bin/env python3
"""Reduce 0.


Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools
import math
from collections import Counter


def calculate_w(key, group,output_re):
    group = list(group)
    # calculate x_mean or y_mean
    w_squared = 0
    for line in group:
        output_re.append(line)
        line = line.replace("\n","")
        docid = line.split("\t")[0]
        line = line.split("\t")[1]
        term = line.split()[0]
        nk = line.split()[2]
        tf = line.split()[1]
        N = line.split()[3]
        tf = int(tf)
        N = int(N)
        nk = int(nk)
        idf  = math.log10(N/nk)
        w = tf * idf
        w_squared += w * w
    return w_squared

def reduce_one_group(output_re,w_squared):
    for line in output_re:
        line = line.replace("\n","")
        docid = line.split("\t")[0]
        line = line.split("\t")[1]
        term = line.split()[0]
        nk = line.split()[2]
        tf = line.split()[1]
        N = line.split()[3]
        tf = int(tf)
        N = int(N)
        nk = int(nk)
        idf  = math.log10(N/nk)
        print(f"{term} {docid} \t {idf} {tf} {w_squared}")
    return 0


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    #group by doc_id
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    w_squared = 0
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        output_re = []
        w_squared = calculate_w(key,group,output_re)
        reduce_one_group( output_re,w_squared)
    # print(count)


if __name__ == "__main__":
    main()