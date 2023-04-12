#!/usr/bin/env python3
"""Reduce 0.


Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools



def reduce_one_group(group):
    '''Reduce one group.'''
    group = list(group)
    # calculate x_mean or y_mean
    n_k = len(group)
    for line in group:
        line = line.replace("\t"," ")
        term = line.split(" ")[0]
        docid = line.split(" ")[1]
        t_f = line.split(" ")[2]
        n_doc = line.split(" ")[3]
        n_doc = int(n_doc)
        t_f = int (t_f)
        # idf  = math.log10(N/n_k)
        # w = t_f * idf
        # w_squared = w * w
        print(f"{docid}\t{term} {t_f} {n_k} {n_doc} ")
    return 0


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    #group by doc_id
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for _, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(group)
    # print(count)


if __name__ == "__main__":
    main()
