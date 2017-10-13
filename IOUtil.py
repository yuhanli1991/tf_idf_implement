from tfidfOper import *
from DButil import *

MATRIX_FILE = "./out/matrix.out"
OUTPUT_FILE = "./out/tfidf.out"
SORTED_MATRIXSUM_FILE = "./out/sortedMatSum.out"
SORTED_BUCKET_FILE = "./out/sortedBucket.out"
SCORE_RANGE = 0.02

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
        return (sorted(templateWeightMap.items(), lambda x, y: cmp(x[1], y[1]), reverse=True), self.getRowList(templateWeightMap))
    def getBucketList(self, weightArray, scoreRange = 0):
        sumMat = self.getSortedMatSum(weightArray)[0]
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
        if range == 0:
            return ret
        else:
            preKey = 0.0
            retRange = []
            tempList = []
            tempScoreList = []
            retScore = []
            for i in ret:
                # print key
                key = i[0]
                value = i[1]
                if preKey - key < scoreRange and preKey - key >= 0.0:
                    tempScoreList.append(key)
                    tempList.append(value)
                else:
                    if tempList:
                        retRange.append(tempList)
                        retScore.append(tempScoreList)
                    tempList = value[:]
                    tempScoreList = [key]
                preKey = key
            retRange.append(tempList)
            return (retScore, retRange)
    def getDictList(self, templateWeightMap):
        NUM_ROWS = 1
        logID = 1
        ret = []
        tempDict = {}
        for temp in templateWeightMap.keys():
            tempDict['LOG_ID'] = logID

            tempDict['LOG_TEMP'] = temp
            tempDict['LOG_TEMP_SCORE'] = templateWeightMap[temp]
            tempDict['LOG_PRIORITY'] = 0
            tempDict['LOG_TYPE'] = 'asm_alert'

            tempDict['LOG_NAME'] = 1
            tempDict['LOG_EXAMPLE'] = ''

            logID += 1
            ret.append(tempDict)
            tempDict = {}
            if logID >= NUM_ROWS:
                break
        return ret
    def getRowList(self, templateWeightMap):
        NUM_ROWS = float("inf")
        logID = 1
        ret = []
        for temp in templateWeightMap.keys():
            row = (logID, temp, templateWeightMap[temp], 0, 'asm_alert', '', '')
            logID += 1
            ret.append(row)
            if logID >= NUM_ROWS:
                break
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
    result = ioutil.getBucketList(weightArray, scoreRange = SCORE_RANGE)
    #ioutil.writeMatrix(result, SORTED_BUCKET_FILE)
    # for i in range(len(result[0])):
    #     score = result[0][i]
    #     temps = result[1][i]
    #     print score, temps
    # print len(result[0])
    templateWeightMap = sortedMatSumList[1]
#    print templateWeightMap
    print len(templateWeightMap)
    
    print templateWeightMap
    db = DButil()
    db.conToDB()


    #db.dropTable("LogTemplateBase")
    #db.executeCmd("create table LogTemplateBase (LOG_ID NUMBER primary key, LOG_NAME VARCHAR2(30), LOG_TEMP VARCHAR2(300), LOG_TEMP_SCORE NUMBER(38,5), LOG_EXAMPLE VARCHAR2(800), LOG_PRIORITY NUMBER, LOG_TYPE VARCHAR2(30))")
    #db.queryDesc("LogTemplateBase")
    # db.executeCmd(
    #     "create table LogTemplateBase2 (LOG_ID NUMBER primary key, LOG_TEMP VARCHAR2(300))")
    #db.insertTemps(templateWeightMap, "LogTemplateBase")
    result = db.executeCmd("select * from LogTemplateBase")
    print result
    print len(result)

    db.closeCon()
    # ioutil.writeMatrix(sortedMatSumList, SORTED_MATRIXSUM_FILE)
    # print type(weightArray)
    # ioutil.writeMatrix(weightArray, OUTPUT_FILE)