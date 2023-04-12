#!/usr/bin/env python3
"""Reduce 0.


Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools



def reduce_one_group( group):
    '''I am a doc string.'''
    group = list(group)
    combined = ''
    for line in group:
        line = line.replace('\n','')
        term = line.split("\t")[0]
        idf_dc_tf_norm = line.split("\t")[1]
        idf = idf_dc_tf_norm.split(" ",1)[0]
        dc_tf_norm = idf_dc_tf_norm.split(" ",1)[1]
        #print(dc_tf_norm)
        combined += " " + dc_tf_norm
    print(f"{term} {idf}\t{combined}")
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
