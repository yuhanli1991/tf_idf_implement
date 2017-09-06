from tfidfOper import *

MATRIX_FILE = "/Users/yuhanli/PycharmProjects/TFIDFImple/out/matrix.out"
OUTPUT_FILE = "/Users/yuhanli/PycharmProjects/TFIDFImple/out/tfidf.out"
SORTED_MATRIXSUM_FILE = "/Users/yuhanli/PycharmProjects/TFIDFImple/out/sortedMatSum.out"

# MATRIX_FILE = "H:\VSProject\TFIDFimple\logs\matrix.out"
# OUTPUT_FILE = "H:\\VSProject\\TFIDFimple\\logs\\tfidf.out"

class IOUtil(object):
    "Do read file by lines"
    def __init__(self, fileName):
        self.target_file = fileName
        self.tempList = []
    def readByLine(self):
        file = open(self.target_file)
        retList = []
        while 1:
            line = file.readline()
            if not line:
                break
            retList.append(line)

        file.close()
        return retList

    def getTmpList(self):
        return self.tempList

    def convertToList(self, readList):
        appList = []
        for line in readList:
            self.tempList.append(line.split(' ~~ ')[0])
            appList.append([int(x) for x in line.split(' ~~ ')[1].split(' - ')[0:-1]])
        return appList
    def writeMatrix(self, matrixList, fileName):
        with open(fileName, "w") as file:
            for i in matrixList:
                k = ' '.join([str(j) for j in i])
                file.write(k + "\n")
            file.close()
    def getSortedMatSum(self, weightArray):
        weightSumList = weightArray.sum(axis=1).tolist()
        templateWeightMap = {}
        for i, tmp in enumerate(self.tempList):
            templateWeightMap[tmp] = weightSumList[i][0]
        # print templateWeightMap
        return sorted(templateWeightMap.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    def getBucketList(self, weightArray):
        sumMat = self.getSortedMatSum(weightArray)
        BucketMap = {}
        for key, value in sumMat:
            if not value in BucketMap:
                BucketMap[value] = [key]
            else:
                BucketMap[value].append(key)
        #ret = []
        #for key in sorted(BucketMap.keys()):
        #    ret.append((key, BucketMap[key]))
        ret = [(key, BucketMap[key]) for key in sorted(BucketMap.keys(), reverse = True)]
        return ret

if __name__ == "__main__":




    ioutil = IOUtil(MATRIX_FILE)
    readList = ioutil.readByLine()
    appList = ioutil.convertToList(readList)
    tfidfIns = tfidfOper()
    weightArray = tfidfIns.transformer(appList)


    # print weightArray
    # print (weightArray.sum(axis=1).tolist())
    # print (ioutil.getTmpList())
    sortedMatSumList = ioutil.getSortedMatSum(weightArray)
    result = ioutil.getBucketList(weightArray)
    for x in result:
        print x
    print len(result)
    # ioutil.writeMatrix(sortedMatSumList, SORTED_MATRIXSUM_FILE)
    # print type(weightArray)
    # ioutil.writeMatrix(weightArray, OUTPUT_FILE)