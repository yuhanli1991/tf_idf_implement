
from sklearn.feature_extraction.text import TfidfTransformer



from numpy import *
class tfidfOper(object):
    def transformer(self, matrixList):
        trans = TfidfTransformer()
        counts = array(matrixList)
        tfidf = trans.fit_transform(counts)
        # print type(tfidf)
        return tfidf
