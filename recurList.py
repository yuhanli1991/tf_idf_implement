import time

start = time.clock()
TEMPLATED_LOGS_LOC = "./templatedLogs/"
EVENT_COUNT_THRESHOLD = 6
FILE_NUMBER = 216
EVENT_MIN_LENGTH = 5
OUTPUT_FILE = "./out/recurList_result.txt"

class recurList(object):


    def __init__(self):
        self.allList = []
        self.dupSub = []

    def getSize (self):
        s = 0
        for f in self.allList:
            s += len(f)
        return s
    def getListAll (self):

        for i in range(1, FILE_NUMBER + 1):
            fileName = TEMPLATED_LOGS_LOC + str(i)
            self.allList.append(self.readByLine(fileName))
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
        if len(listA) != len(listB):
            return False
        for i in range(len(listA)):
            if listA[i] != listB[i]:
                return False
        return True

    def delSubList (self, ls, begin, end):
        l = ls[:]
        for i in range (begin, end + 1):
            try:
                del ls[begin]
            except:
                print ('Out of index')
                print (len(l))
                print (ls)
                print (begin)
                print (end)
                exit()

    def delAllSubList (self, ls):
        for fileNum in range(FILE_NUMBER):
            tmpList = self.allList[fileNum]
            lineNum = 0
            #for lineNum in range(len(tmpList) - len(ls) + 1):
            while lineNum < len(tmpList) - len(ls) + 1:
                if self.compareList(tmpList[lineNum : lineNum + len(ls)], ls):
                    self.delSubList(tmpList, lineNum, lineNum + len(ls) - 1)
                else:
                    lineNum += 1

    def removeDupSub (self, dupSub):
        for x in dupSub:
            self.setNullBatch(self.allList[x[0]], x[1], x[2] - 1)
        self.removeNullBatch()

    def setNullBatch (self, ls, begin, end):
        for i in range (begin, end):
            ls[i] = ''

    def removeNullBatch (self):
        for f in self.allList:
            line = 0
            while line < len (f):
                if f[line] == "":
                    del f[line]
                else:
                    line += 1



    def recurList (self):
        ret = {}
        # count = 1
        # pre = False
        # preList = []
        # preCount = 1
        for fileNum in range(FILE_NUMBER):
            tmpList = self.allList[fileNum]
            lineNum = 0
            # for lineNum in range(len(tmpList)):
            while lineNum < len(tmpList):
                pre = False
                preList = []
                preCount = 1
                listLen = EVENT_MIN_LENGTH
                preDupSub = []
                # for listLen in range(3, len(tmpList) - lineNum):
                while listLen < len(tmpList) - lineNum:
                    begin, end = lineNum, lineNum + listLen
                    targetList = tmpList[begin : end]
                    count = self.targetMatch(targetList, fileNum, lineNum)
                    if count > 0:
                        preList = targetList
                        preCount = count
                        pre = True
                        preDupSub = self.dupSub
                    elif count == 0 and pre == True:
                        # self.delAllSubList(preList)
                        self.removeDupSub(preDupSub)
                        ret[','.join(preList)] = preCount
                        break
                    elif count == 0 and pre == False:
                        self.delSubList(tmpList, lineNum, lineNum + listLen - 1)
                        break
                    listLen += 1
                if count > 0:
                    self.removeDupSub(preDupSub)
                    ret[','.join(preList)] = preCount
                lineNum += 1
        return ret


    # return: count, if 0 means it's not a event
    def targetMatch (self, targetList, fileNum, lineNum):
        self.dupSub = []
        count = 1
        listLen = len(targetList)
        beginLine = lineNum + listLen
        for f in range(fileNum, FILE_NUMBER):
            for l in range(beginLine, len(self.allList[f]) - listLen + 1):
                head, tail = l, l + listLen
                srcList = self.allList[f][head : tail]
                if (self.compareList(targetList, srcList)):
                    # self.delSubList(self.allList[f], head, tail - 1)
                    count += 1
                    self.dupSub.append((f, head, tail))
            beginLine = 0
        if count >= EVENT_COUNT_THRESHOLD:
            return count
        else:
            return 0


    def writeResult (self, result, file):
        with open(file, "w") as f:
            for key in result.keys():
                for tmp in key.split(','):
                    f.write(tmp)
                f.write(str(result[key]))
                f.write("\n===========================\n")
            f.close()


if __name__ == "__main__":
    recurlist = recurList()
    recurlist.getListAll()
    print (recurlist.getSize())
    result = recurlist.recurList()
    print (result)
    print (result.values())
    print (len(result))
    recurlist.writeResult(result, OUTPUT_FILE)


    elapsed = (time.clock() - start)
    print("Time used:", elapsed)
