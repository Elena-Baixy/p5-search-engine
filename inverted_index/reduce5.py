#!/usr/bin/env python3

"""Reduce0."""
import sys
import itertools


def order(group, combined):
    """I am a doc."""
    group = list(group)
    for line in group:
        line = line.replace("\n", "")
        # line = line.replace("\t ","")
        key = line.split("\t")[0]
        line = line.split("\t")[1]
        term = line.split(" ", 1)[0]
        value = line.split(" ", 2)[2]
        term_pair = key + " " + term
        if term_pair not in combined:
            combined[term_pair] = line
        else:
            combined[term_pair] = combined[term_pair] + " " + value
        # print(term_pair + " " + combined[term_pair] + " " +value)


def reduce_one_group(group):
    """I ma a doc."""
    group = list(group)
    for line in group:
        line = line.replace("\n", "")
        ouputval = line.split("\t")[1]
        print(f"{ouputval}")
    # for term_pair in combined:
    #     print(f"{combined[term_pair]}")


def keyfunc(line):
    """Return the key from a TAB-delimited key-value pair."""
    return line.partition("\t")[0]


def main():
    """Divide sorted lines into groups that share a key."""
    # combined = {}
    for _, group in itertools.groupby(sys.stdin, keyfunc):
        # order(key, group,combined)
        reduce_one_group(group)
    # print(count)


if __name__ == "__main__":
    main()
