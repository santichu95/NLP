"""
Santiago Andaluz Ruiz
Natural Language processing
2/10/2017
"""

import nltk
import math
from scipy import spatial

class CorpusReader_TFIDF:
    def __init__(self, corpus, tf="frequency", idf="Base",
                 stopword="fileName", stemmer=nltk.PorterStemmer(), ignorecase="yes"):
        # Parameters
        self.corpus = corpus
        self.termFreq = tf 
        self.inverseFreq = idf
        self.stop = stopword
        self.stemmer = stemmer
        self.ignorecase = ignorecase

        self.root = self.corpus.root

        #Storing the list of fileids
        self.fileid = self.corpus.fileids()


        #Getting a list of all the words in the corpus
        self.wordList = self.collectWords()
        if ignorecase == "yes":
            self.wordList = [x.lower() for x in self.wordList]

        #list of all the tfidf vectors
        self.idf = [0] * len(self.wordList)
        self.vectors = [[0] * len(self.wordList) for x in range(0, len(self.fileid))]

        #Stemming
        self.wordList = [self.stemmer.stem(x) for x in self.wordList]

        self.calcAll()

    def calcDoc(self, fId):
        #Get and proccess all the words from the specific document
        wList = self.words(fId)
        if self.ignorecase == "yes":
            wList = [x.lower() for x in wList]
        wList = [self.stemmer.stem(x) for x in wList]
        wList.sort()

        #find the index of the specific file
        fIndex = self.fileid.index(fId);
        prev = None

        #calculate tf and idf for word in the document
        for word in wList:
            try: 
                wIndex = self.wordList.index(word)
                if prev != word:
                    self.idf[wIndex] += 1
                    prev = word
                self.vectors[fIndex][wIndex] += 1
            except ValueError:
                pass

        return None

    def calcAll(self):
        #Calculate tf and idf for all the documents
        for f in self.fileid:
            self.calcDoc(f)

        #Calculate tfidf score for each document
        for f in self.fileid:
            self.calcTfidf(f)
        return None

    #Calculates the actual tfidf score for every document
    def calcTfidf(self,f):
        numDocs = len(self.fileid)
        foundBase = 0
        if ( self.inverseFreq == "Smoothed" ):
            foundbase = 1;
        elif ( self.inverseFreq == "LimitedSmooth"):
            foundbase = 1.0/numDocs
        elif ( self.inverseFreq == "DoubleSmooth"):
            foundbase = 1
            numDocs += 1

        counter = 0
        fIndex = self.fileid.index(f)
        for w in self.wordList:
            if ( (self.idf[counter] + foundBase) != 0 ):
                idfValue = math.log2(float(numDocs)/(foundBase + self.idf[counter]))
                self.vectors[fIndex][counter] *= idfValue
                counter += 1
            else:
                self.vectors[fIndex][counter] *= 0
                counter += 1

    def fileids(self, categories=None):
        if categories is not None:
            return self.corpus.fileids(categories)
        else:
            return self.corpus.fileids()

    def categories(self, fileids=None):
        if fileids is not None:
            return self.corpus.categories(fileids)
        else:
            return self.corpus.categories()

    def raw(self, fileids=None, categories=None):
        if fileids is not None:
            return self.corpus.raw(fileids)
        elif categories is not None:
            return self.corpus.raw(categories=categories)
        else:
            return self.corpus.raw()

    def words(self, fileids=None, categories=None):
        if fileids is not None:
            return self.corpus.words(fileids)
        elif categories is not None:
            return self.corpus.words(categories=categories)
        else:
            return self.corpus.words()

    def sents(self, fileids=None, categories=None):
        if fileids is not None:
            return self.corpus.sents(fileids)
        elif categories is not None:
            return self.corpus.sents(categories=categories)
        else:
            return self.corpus.sents()

    def abspath(self,fileid):
        return self.corpus.abspath(fileid)

    def encoding(self,fileid):
        return self.corpus.encoding(fileid)

    def open(self,fileid):
        return self.corpus.open(fileid)

    def readme(self):
        return self.corpus.readme()

    def tf_idf(self, fileid=None, filelist=None):
        if fileid is not None:
            return self.vectors[self.fileid.index(fileid)]
        elif filelist is not None:
            temp = []
            for fId in filelist:
                temp.append(self.vectors[self.fileid.index(fileid)])
            return temp
        return self.vectors

    def tf_idf_dim(self):
        return self.wordList
    
    def tf_idf_new(words):
        tfidf = [0] * self.wordList
        wList = words
        if self.ignorecase == "yes":
            wList = [x.lower() for x in wList]
        wList = [self.stemmer.stem(x) for x in wList]
        wList.sort()

        for word in wList:
            try: 
                wIndex = self.wordList.index(word)
                ifidf[wIndex] += 1
            except ValueError:
                pass

        numDocs = len(self.fileid)
        foundBase = 0
        if ( self.inverseFreq == "Smoothed" ):
            foundbase = 1;
        elif ( self.inverseFreq == "LimitedSmooth"):
            foundbase = 1.0/numDocs
        elif ( self.inverseFreq == "DoubleSmooth"):
            foundbase = 1
            numDocs += 1

        counter = 0
        for w in self.wordList[0:15]:
            if ( (self.idf[counter] + foundBase) != 0 ):
                idfValue = math.log2(float(numDocs)/(foundBase + self.idf[counter]))
                tfidf[counter] *= idfValue
                counter += 1
            else:
                tfidf[counter] *= 0
                counter += 1
        return tfidf

    def cosine_sim(self,fileid):
        fIndex1 = self.fileid.index(fileid[0])
        fIndex2 = self.fileid.index(fileid[1])

        return 1 - spatial.distance.cosine(self.vectors[fIndex1], self.vectors[fIndex2])

    #Get all the words for a specific corpus
    def collectWords(self):
        try:
            return list(set(self.corpus.words()))
        except TypeError:
            for fId in self.fileid:
                wList = []
                wList.extend(self.corpus.words(fId))
            return list(set(wList))
        
