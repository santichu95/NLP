import nltk
from nltk.corpus import wordnet as wn

def get_synsets(term):
    return wn.synsets(term, pos=[wn.NOUN, wn.VERB])

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
