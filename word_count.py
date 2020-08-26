# word_count.py
# ===================================================
# Implement a word counter that counts the number of occurrences of all the words in a file. The word
# counter will return the top X words, as indicated by the user.
# ===================================================
# Author: Christine Pham

import re
from hash_map import HashMap

"""
This is the regular expression used to capture words. It could probably be endlessly
tweaked to catch more words, but this provides a standard to can test against.
"""
rgx = re.compile("(\w[\w']*\w|\w)")

def hash_function_2(key):
    """
    This is a hash function used for the hashmap.
    """

    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash

def top_words(source, number):
    """
    Takes a plain text file and counts the number of occurrences of case insensitive words.
    Returns the top `number` of words in a list of tuples of the form (word, count).

    Args:
        source: the file name containing the text
        number: the number of top results to return (e.g. 5 would return the 5 most common words)
    Returns:
        A list of tuples of the form (word, count), sorted by most common word. (e.g. [("a", 23), ("the", 20), ("it", 10)])
    """

    keys = set()

    ht = HashMap(2500, hash_function_2)

    # This block of code will read a file one word as a time
    with open(source) as f:
        for line in f:
            words = rgx.findall(line)
            for w in words:
                # check if word is already in hash map (ht). if none, create an entry with value as 1
                if ht.contains_key(w) is False:
                    ht.put(w, 1)
                # if True, value += 1
                else:
                    val = ht.get(w)
                    ht.put(w, val+1)

                # put the word in the set keys
                keys.add(w.lower())

    # create empty array, push pair values of keys in
    pairs = [(word, ht.get(word)) for word in keys]

    # sort the array, slice the array by number given
    pairs = sorted(pairs, key=lambda x: x[1], reverse=True)

    return pairs[:number]


#print(top_words("alice.txt",10))
