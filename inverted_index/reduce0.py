#!/usr/bin/env python3
"""Reduce 0.
Template reducer.
https://github.com/eecs485staff/madoop/blob/main/README_Hadoop_Streaming.md
"""
import sys
import itertools


def reduce_one_group(key, group):
    group = list(group)
    count = 0
    for row in group:
        row = row.replace("\t ","")
        row = row.replace("\n","")
        num = row.split(" ")[1]
        count += int(num)
    print(count)
    return 0


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    # 这里其实就是一个数字都不用group但是她非要keyfunc return一个delimiter 
    # 这个line.split()[0]在很大的input.csv print的数字应该是3268 但是现在是112
    return line.split()[0]


def main():
    """Divide sorted lines into groups that share a key."""
    count = 0
    for key, group in itertools.groupby(sys.stdin, keyfunc):
        # count +=1
        reduce_one_group(key, group)
    # print(count)


if __name__ == "__main__":
    main()
