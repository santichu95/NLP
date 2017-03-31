#Santiago Andaluz Ruiz
#CSI 4v96
#Natural Language Processing

import queue
from nltk.corpus import wordnet as wn


#Antonym path similarity
def ant_path_similarity(s,t):
    lLemma = s.lemmas()
    rLemma = t.lemmas()

    print(lLemma)
    anty = set()

    for lem in s.lemmas():
        [anty.add(x) for x in lem.antonyms()]

    largest = -1
    for ant in rLemma:
        if ant in anty:
            current = adj_path_similarity(t, ant.synset())
            if current > largest:
                largest = current
    return largest

def symant_path_similarity(s,t):
    return max(ant_path_similarity(s,t), ant_path_similarity(t,s))

def word_symant_path_similarity(s,t):
    left = get_adj_synsets(s)
    right = get_adj_synsets(t)

    if len(left) == 0 or len(right) == 0:
        return []

    result = []
    largest = -1
    current = 0.0
    for lSense in left:
        for rSense in right:
            current = symant_path_similarity(lSense,rSense)
            if current > largest:
                result = [(lSense, rSense, current)]
                largest = current
            elif current == largest:
                result.extend((lSense, rSense, current))

    return result

def word_ant_path_similarity(s,t):
    left = get_adj_synsets(s)
    right = get_adj_synsets(t)

    if len(left) == 0 or len(right) == 0:
        return []

    result = []
    largest = -1
    current = 0.0
    for lSense in left:
        for rSense in right:
            current = ant_path_similarity(lSense,rSense)
            if current > largest:
                result = [(lSense, rSense, current)]
                largest = current
            elif current == largest:
                result.extend((lSense, rSense, current))

    return result


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

def att_path_similarity(s,t):
    sPrime = s.attributes()
    tPrime = t.attributes()
    if len(sPrime) == 0 or len(tPrime) == 0:
        return 0

    largest = 0
    for left in sPrime:
        for right in tPrime:
            current = left.path_similarity(right)
            if current > largest:
                largest = current

    return largest

def word_att_path_similarity(s,t):
    left = get_adj_synsets(s);
    right = get_adj_synsets(t);

    if len(left) == 0 or len(right) == 0:
        return []

    result = []
    largest = -1
    current = 0.0
    for lSense in left:
        for rSense in right:
            current = att_path_similarity(lSense,rSense)
            if current > largest:
                result = [(lSense, rSense, current)]
                largest = current
            elif current == largest:
                result.extend((lSense, rSense, current))

    return result

def word_adj_path_similarity(s,t):
    left = get_adj_synsets(s);
    right = get_adj_synsets(t);

    if len(left) == 0 or len(right) == 0:
        return []

    result = []
    largest = -1
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
