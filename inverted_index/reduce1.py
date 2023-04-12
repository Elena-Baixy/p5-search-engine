#!/usr/bin/env python3
"""Reduce 0.


Template reducer.

https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools



def reduce_one_group(group,total_docu_count):
    """Format {docid} {token}\t {total_docu_count}"""
    group = list(group)
    for line in group:
        line = line.replace("\n","")
        line = line.replace("\t"," ")
        doc_id = line.split(" ")[0]
        term = line.split(" ")[1]
        t_f = line.split(" ")[2]
    print(f"{doc_id} {term}\t{t_f} {total_docu_count}")
    return 0


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    #group by doc_id
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    with open('total_document_count.txt', 'r',encoding='utf-8') as file:
        total_docu_count = file.readline().strip()
    for _, group in itertools.groupby(sys.stdin, keyfunc):
        reduce_one_group(group, total_docu_count)
    # print(count)


if __name__ == "__main__":
    main()
