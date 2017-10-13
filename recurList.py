
TEMPLATED_LOGS_LOC = "./templatedLogs/"
EVENT_COUNT_THRESHOLD = 5

class recurList(object):
    def __init__(self):
        self.allList = []

    def getListAll (self):

        for i in range(1, 217):
            fileName = TEMPLATED_LOGS_LOC + str(i)
            self.allList[i - 1] = self.readByLine(fileName)
        return self.allList

    def readByLine(self, fileName):
        file = open(fileName)
        retList = []
        while 1:
            line = file.readline()
            if not line:
                break
            retList.append(line)

        file.close()
        return retList

    # args: list, list
    # return: boolean
    def compareList (self, listA, listB):
        if (len(listA) != len(listB)):
            return False
        for i, j in listA, listB:
            if i != j:
                return False
        return True

    def delSubList (self, ls, begin, end):
        for i in range (begin, end + 1):
            del ls[begin]

    def recurList (self):
        ret = {}
        count = 1
        pre = False
        preList = []
        preCount = 1
        for fileNum in range(216):
            tmpList = self.allList[fileNum]
            for lineNum in range(len(tmpList)):
                for listLen in range(3, len(tmpList) - lineNum):
                    begin, end = lineNum, lineNum + listLen
                    targetList = tmpList[begin : end]
                    count = self.targetMatch(targetList, fileNum, lineNum)
                    if count > 0:
                        preList = targetList
                        preCount = count
                        pre = True
                        continue
                    elif count == 0 and pre == True:
                        ret[preList] = preCount
                        moveToNextBatch
                    elif count == 0 and pre == False:
                        moveToNextBatch



    # return: count, if 0 means it's not a event
    def targetMatch (self, targetList, fileNum, lineNum):
        count = 1
        listLen = len(targetList)
        beginLine = lineNum + listLen
        for f in range(fileNum, 216):
            for l in range(beginLine, len(self.allList[f]) - listLen + 1):
                head, tail = l, l + listLen
                srcList = self.allList[f][head : tail]
                if (self.compareList(targetList, srcList)):
                    count += 1
                    if count > EVENT_COUNT_THRESHOLD:
                        return count

            beginLine = 0
        return 0

