#!/usr/bin/env python3

"""Reduce0."""
import sys
import itertools


def reduce_one_group(group):
    """I ma a doc."""
    group = list(group)
    count = 0
    for row in group:
        row = row.replace("\t ", "")
        row = row.replace("\n", "")
        num = row.split(" ")[1]
        count += int(num)
    print(count)
    return 0


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.split()[0]


def main():
    """Divide sorted lines into groups that share a key."""
    for _, group in itertools.groupby(sys.stdin, keyfunc):
        # count +=1
        reduce_one_group(group)
    # print(count)


if __name__ == "__main__":
    main()
