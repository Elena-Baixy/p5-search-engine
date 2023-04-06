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
    id_word = {}
    for line in group:
        # print(line)
        docAndTerm = line.partition("\t")[0]
        total_docu_count = line.partition("\t")[2].strip()
        # print(total_docu_count)
        if docAndTerm in id_word.keys():
            id_word[docAndTerm] +=1
        else:
            id_word[docAndTerm] = 1
            
    for key,tf in id_word.items():
        docid = key.split(",")[0][2]
        term = key.split(",")[1].split("'")[1]
        print(f"{docid} {term} \t {tf} {total_docu_count}")
    # print(id_word)
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