"""
Santiago Andaluz Ruiz
Natural Language processing
2/10/2017
"""
import nltk
from nltk.corpus import *
from CorpusReader_TFIDF import CorpusReader_TFIDF

def testCorpus(title, corpus):
    test = CorpusReader_TFIDF(corpus)

    print(title)

    print(test.tf_idf_dim()[0:15])
    for fileId in test.fileids():
        fIndex = test.fileid.index(fileId)
        print(fileId, end=', ')
        print(' '.join(str(v) for v in test.vectors[fIndex][0:15]))

    #Print all the cosine similarities of all the 
    for fileId in test.fileids():
        for fId in test.fileids():
            print(fileId, fId, end=' ')
            print(test.cosine_sim([fileId,fId]))

def test():
    testCorpus("Brown", brown)
    testCorpus("Shakespeare", shakespeare)
    testCorpus("State of The Union", state_union)

test()
