import networkx as nx
import queue
from nltk.corpus import wordnet as wn
from networkx import *

def test():
    adjList = wn.all_synsets('a')
    G = nx.Graph();

    seen = set()

    for synset in adjList:
        for word in synset.similar_tos():
            if word not in seen:
                seen.add(word)
                G.add_edge(synset,word)

    result = nx.all_pairs_shortest_path_length(G)
        
    largest = 0;
    for key in result.values():
        if ( max(key.values()) > largest ):
            largest = max(key.values())
            print(max(key.values()))
            print(key)


def adj_path_similarity(s,t):

    q = queue.Queue()
    seen = set()

    q.put((s, 0))
    seen.add(s)
    while not q.empty():
        word = q.get()
        for synset in word[0].similar_tos():
            if synset == t:
                return (1.0/(word[1]+2))
            if synset not in seen:
                seen.add(synset)
                q.put((synset, word[1] + 1))

    return 0;

def word_adj_path_similarity(s,t):
    left = get_adj_synsets(s);
    right = get_adj_synsets(t);

    result = []
    largest = 0.0
    current = 0.0
    for lSense in left:
        for rSense in right:
            current = adj_path_similarity(lSense,rSense)
            if current > largest:
                result = [(lSense, rSense, current)]
                largest = current
            elif current == largest:
                result.extend((lSense, rSense, current))

    return result
        

def get_synsets(term):
    return wn.synsets(term, pos=[wn.NOUN, wn.VERB])

def get_adj_synsets(term):
    return wn.synsets(term, pos=[wn.ADJ])

def word_similarity(function, s,t,simulate_root=True):
    left = get_synsets(s);
    right = get_synsets(t);

    result = []
    largest = 0.0
    current = 0.0
    for lSense in left:
        for rSense in right:
            current = function(lSense,rSense,simulate_root)
            if current > largest:
                result = [(lSense, rSense, current)]
                largest = current
            elif current == largest:
                result.extend((lSense, rSense, current))

    return result

def word_path_similarity(s,t,simulate_root=True):
    return word_similarity(wn.path_similarity, s, t, simulate_root)

def word_lch_similarity(s,t,simulate_root=True):
    return word_similarity(wn.lch_similarity, s, t, simulate_root)

def word_wup_similarity(s,t,simulate_root=True):
    return word_similarity(wn.wup_similarity, s, t, simulate_root)
