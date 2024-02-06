import numpy as np
from typing import *
from dataclasses import dataclass
import unittest
import string

calpoly_email_address = "chartl03@calpoly.edu"

def make_hash(size):
    hash_table = [None] * size
    return hash_table


def h(string, hash_table):
    n = min(len(string), 8)
    total = 0
    for item in range(len(string) - 1):
        total = (total + (ord(string[item]) * (31 ** (n - 1 - item)))) % len(hash_table)
    return int(total)


def put(item, hash_table):
    index = int(h(item, hash_table))
    if hash_table[index] is None:
        hash_table[index] = item
    else:
        step = 1
        next_index = (index + step) % len(hash_table)
        while next_index != index and hash_table[int(next_index)] is not None:
            step += 1
            next_index = (index + (step * (step + 1)) / 2) % len(hash_table)

        if next_index == index:
            print("Hash table is full, unable to insert:", item)
        else:
            hash_table[int(next_index)] = item
    load = hash_table.count(None)
    print(load)
    if (load * 2) <= len(hash_table):
        extension = [None] * len(hash_table)
        hash_table.extend(extension)


def contains(item, hash_table):
    index = int(h(item, hash_table))
    start_index = index
    step = 1
    while hash_table[index] is not None:
        if hash_table[index] == item:
            return True
        step += 1
        index = int((index + (step * (step + 1)) / 2) % len(hash_table))
        if index == start_index:
            break
    return False


def file_hash(filename, hash_table):
    with open(filename, "r") as f:
        check_list = []
        for line in f:
            line = line.strip()
            line = line.split()
            for word in line:
                if word not in check_list:
                    put(word, hash_table)
                    check_list.append(word)
                    print(check_list)
    return hash_table


def hash_lists(hash_table):
    htable_lists = []
    for item in hash_table:
        list_item = [item]
        htable_lists.append(list_item)
    return htable_lists


def word_concordance(hash_table, filename):
    with open(filename, 'r') as f:
        for line_num, line in enumerate(f, start=1):
            for item in hash_table:
                if item[0] is not None:
                    if item[0] in line:
                        item.append(line_num)
    return hash_table



def clean_hash(hash_table):
    for item in hash_table:
        if item[0] is not None:
            clean_item = item[0].translate(str.maketrans("", "", string.punctuation)).lower()
            item[0] = clean_item
        else:
            item[0] = item[0]
    return hash_table


def stop_concordance(stop_file, hash_table):
    stop_hash = make_hash(128)
    stop_hash = file_hash(stop_file, stop_hash)
    stop_hash = hash_lists(stop_hash)

    for item in hash_table:
        # Check if the item is not None before attempting to compare
        if item is not None:
            for word in stop_hash:
                if word is not None:
                    if item[0] == word[0]:
                        hash_table.remove(item)
                        break  # Exit inner loop after removing the item

    return hash_table



def write_new_file(hash_table, write_file):
    for item in hash_table:
        with open(write_file, 'a') as a:
            if item[0] is not None:
                lines = "".join(str(item[1:]))
                a.write(item[0] + ': ' + lines + '\n')


def concordance(stop_file, read_file, write_file):
    read_hash = make_hash(128)
    read_hash = file_hash(read_file, read_hash)
    read_hash = hash_lists(read_hash)
    read_hash = stop_concordance(stop_file, read_hash)
    read_hash = word_concordance(read_hash, read_file)
    read_hash = clean_hash(read_hash)
    write_new_file(read_hash, write_file)



# Make a fresh hash table with the given size, containing no elements
def test_hash(size: int):
    hash_table = [None] * size
    return hash_table


# Return the size of the given hash table
def hash_size(hash_table):
    return len(hash_table)


# Return the number of elements in the given hash table
def hash_count(hash_table):
    elements = 0
    for item in hash_table:
        if item is not None:
            elements += 1
        else:
            elements += 0
    return elements


# Does the hash table contain a mapping for the given word?
def has_key(hash_table, word):
    contains(word, hash_table)


# What line numbers is the given key mapped to in the given hash table?
# this list should not contain duplicates, but need not be sorted.
def lookup(hash_table, word):
    for item in hash_table:
        if item is not None:
            if item == word:
                return item[1:]


# Add a mapping from the given word to the given line number in
# the given hash table
def add(hash_table, word: str, line: int) -> None:
    put(word, hash_table)
    for item in hash_table:
        if item == word:
            item = [item, line]



# What are the words that have mappings in this hash table?
# this list should not contain duplicates, but need not be sorted.
def hash_keys(hash_table):
    word_list = []
    for item in hash_table:
        if item is not None:
            word_list.append(item)


# given a list of stop words and a list of strings representing a text,
# return a hash table
def make_concordance(words, lines):
    hash_table = test_hash(128)
    for item in range(len(words)):
        add(hash_table, words[item], lines[item])

    return hash_table
