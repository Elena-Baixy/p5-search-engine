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

    id_word = {}
    # print(key)
    
    for line in group:
        # of format {docid} {token}\t {total_docu_count}
        
        docid = line.split()[0]
        term = line.split()[1]
        total_docu_count = line.split()[2]

        docid, term, total_docu_count =  line.split()
        doc_term = (docid,term)

        if doc_term in id_word.keys():
            id_word[doc_term] +=1
        else:
            id_word[doc_term] = 1

    # print(id_word)
    for key,tf in id_word.items():
        docid = key[0]
        term = key[1]
        print(f"{docid} {term} \t {tf} {total_docu_count}")
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