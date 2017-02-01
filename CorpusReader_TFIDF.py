class CorpusReader_TFIDF:
    def __init__(self, corpus, tf="frequency", idf="Base",
                 stopword="fileName", stemmer="nltk.stem.porter", ignorecase="yes"):
        print(corpus, tf, idf, stopword, stemmer, ignorecase)

    def fileids(self, categories=None):
        self.corpus.fileids(categories)

    def categories(self, fileids=None):
        self.corupus.categories(fileids)

    def raw(self, fileids=None, categories=None):
        if fileids is not None:
            self.corpus.raw(fileids=fileids)
        elif categories is not None:
            self.corpus.raw(categories=categories)
        else:
            self.corpus.raw()
