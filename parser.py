# Faiyaz Hasan 

import nltk
import sys
from nltk import word_tokenize
import re

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S | VP NP 
NP -> N | Det N | Det AdjP N | NP PP 
AdjP -> Adj | Adj AdjP 
VP -> V | V NP | V PP | Adv VP | VP Adv
PP -> P NP 
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # tokenize the sentence and excluding any word that doesn’t contain at least one alphabetic character
    tokenized_sentence = word_tokenize(sentence.lower()) 
    letter = [] 
    for elem in tokenized_sentence: 
        if re.search('[a-zA-Z]+', elem) != None:
            letter.append(elem)
    
    return letter 

def isN(t):
    return t.label() == 'N'

def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunk = []

    # Add parent pointers for tree
    tree_with_parent_pointers = nltk.tree.ParentedTree.convert(tree)

    # NP rules have N in common (except NP PP) and so parent of N labels will be NP labels
    for subtree in tree_with_parent_pointers.subtrees(lambda x: x.label() == 'N'):
        chunk.append(subtree.parent())
    
    return chunk

if __name__ == "__main__":
    main()