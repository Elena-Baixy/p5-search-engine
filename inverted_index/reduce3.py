#!/usr/bin/env python3
"""Reduce 0.


Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools
import math


def calculate_w(group,output_re):
    '''I am a doc string.'''
    group = list(group)
    # calculate x_mean or y_mean
    w_squared = 0
    for line in group:
        output_re.append(line)
        line = line.replace("\n","")
        line = line.split("\t")[1]
        n_k = line.split()[2]
        t_f = line.split()[1]
        n_doc = line.split()[3]
        t_f = int(t_f)
        n_doc = int(n_doc)
        n_k = int(n_k)
        idf  = math.log10(n_doc/n_k)
        weight = t_f * idf
        w_squared += weight * weight
    return w_squared

def reduce_one_group(output_re,w_squared):
    '''I am a docstring.'''
    for line in output_re:
        line = line.replace("\n","")
        docid = line.split("\t")[0]
        line = line.split("\t")[1]
        term = line.split()[0]
        n_k = line.split()[2]
        t_f = line.split()[1]
        n_doc = line.split()[3]
        t_f = int(t_f)
        n_doc = int(n_doc)
        n_k = int(n_k)
        idf  = math.log10(n_doc/n_k)
        print(f"{term},{idf}\t{docid} {t_f} {w_squared}")
    return 0


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    #group by doc_id
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    w_squared = 0
    for _, group in itertools.groupby(sys.stdin, keyfunc):
        output_re = []
        w_squared = calculate_w(group,output_re)
        reduce_one_group( output_re,w_squared)
    # print(count)


if __name__ == "__main__":
    main()
