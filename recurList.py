import time
import pickle
from LCS_solution import *
from DButil import *
from UnionFound import *

start = time.clock()
TEMPLATED_LOGS_LOC = "./templatedLogs/"
TEMPLATED_LOGS_ID_LOC = "./pickleBase/templateID.pickle"
TEMP_ID_MAP = "./pickleBase/idMap.pickle"
EVENT_COUNT_THRESHOLD = 6
FILE_NUMBER = 216
EVENT_MIN_LENGTH = 5
EVENT_MAX_LENGTH = 30
OUTPUT_FILE = "./out/recurList_result.txt"
OUTPUT_ID_FILE = "./out/recurList_result_id.txt"
TEMPLATE_BASE = "./asm_alertTemplate.txt"
CLASSIFY_RESULT = "./out/classify_result.txt"
CALSSIFY_DETAIL = "./out/classify_detail.txt"

class recurList(object):


    def __init__(self):
        self.allList = []
        self.dupSub = []
        self.idMap = {}
        self.allIDList = []

    def getSize (self):
        s = 0
        for f in self.allList:
            s += len(f)
        return s

    # Return all templates files as list
    def getListAll (self):

        for i in range(1, FILE_NUMBER + 1):
            fileName = TEMPLATED_LOGS_LOC + str(i)
            self.allList.append(self.readByLine(fileName))
        return self.allList


    def getListAllFromPickle (self):
        self.allList = pickle.load(open(TEMPLATED_LOGS_ID_LOC, "r"))
        print (len(self.allList))

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

    def _createTmpID(self):
        tmpList = self.readByLine(TEMPLATE_BASE)
        for i in range(len(tmpList)):
            self.idMap[tmpList[i]] = i
        pickle.dump(self.idMap, open(TEMP_ID_MAP, "w"))


    def convertToID(self):
        self._createTmpID()

        for f in self.allList:
            tmpIDList = []
            for l in f:
                try:
                    id = self.idMap[l]

                    if tmpIDList and tmpIDList[-1] != id:   #Remove duplicate lines if they are neighboured
                        tmpIDList.append(id)
                    elif not tmpIDList:
                        tmpIDList.append(id)

                except:
                    print ("Hit error when get log line's ID:")
                    print (l)
                    exit(1)
            self.allIDList.append(tmpIDList)
        pickle.dump(self.allIDList, open(TEMPLATED_LOGS_ID_LOC, "w"))


    def convertFromID (self, ls):
        tmpMap = {}
        tmpList = self.readByLine(TEMPLATE_BASE)
        for i in range(len(tmpList)):
            tmpMap[i] = tmpList[i]
        retList = []

        for event in ls:
            l = []
            for id in event:
                line = tmpMap[int(id)]
                l.append(line)
            l.append('=============')
            retList.append(l[:])

        self.writeList(retList, "./out/tmp.out")


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
            ls[i] = -1

    def removeNullBatch (self):
        for f in self.allList:
            line = 0
            while line < len (f):
                if f[line] == -1:
                    del f[line]
                else:
                    line += 1


    def recurList (self):
        keys = self.readByLine(TEMPLATE_BASE)
        ret = {}
        # count = 1
        # pre = False
        # preList = []
        # preCount = 1
        for fileNum in range(FILE_NUMBER):
            tmpList = self.allList[fileNum]
            lineNum = 0

            with open(OUTPUT_FILE, "w") as outFile:


                # for lineNum in range(len(tmpList)):
                while lineNum < len(tmpList):
                    pre = False
                    preList = []
                    preCount = 1
                    listLen = EVENT_MIN_LENGTH
                    preDupSub = []
                    count = 0
                    # for listLen in range(3, len(tmpList) - lineNum):
                    while listLen < len(tmpList) - lineNum and listLen <= EVENT_MAX_LENGTH:
                        begin, end = lineNum, lineNum + listLen
                        targetList = tmpList[begin : end]
                        count = self.targetMatchByDupSub(targetList, fileNum, lineNum)

                        print (self.getSize())
                        # print (listLen, count, count == 0 and pre == True)
                        # print preDupSub
                        # print self.dupSub

                        if count > 0:
                            preList = targetList
                            preCount = count
                            pre = True
                            preDupSub = self.dupSub[:]
                        elif count == 0 and pre == True:
                            # self.delAllSubList(preList)
                            self.removeDupSub(preDupSub)
                            ret[str(preList)] = preCount


                            for l in preList:
                                outFile.write(keys[l])
                            outFile.write(str(preCount))
                            outFile.write("\n================\n")

                            self.dupSub = []
                            break
                        elif count == 0 and pre == False:
                            self.delSubList(tmpList, lineNum, lineNum + listLen - 1)
                            self.dupSub = []
                            break
                        listLen += 1
                        # print (fileNum, lineNum, listLen, count)

                    if count > 0:
                        self.removeDupSub(preDupSub)
                        ret[str(preList)] = preCount
                    lineNum += 1
            outFile.close()
        return ret


    # return: count, if 0 means it's not a event
    def targetMatch (self, targetList, fileNum, lineNum):
        # self.dupSub = []
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

    def targetMatchByDupSub (self, targetList, fileNum, lineNum):
        count = 1
        listLen = len(targetList)
        beginLine = lineNum + listLen
        if not self.dupSub:
            for f in range(fileNum, FILE_NUMBER):
                for l in range(beginLine, len(self.allList[f]) - listLen + 1):
                    head, tail = l, l + listLen
                    srcList = self.allList[f][head: tail]
                    if (self.compareList(targetList, srcList)):
                        # self.delSubList(self.allList[f], head, tail - 1)
                        count += 1
                        self.dupSub.append([f, head, tail])
                beginLine = 0
        else:
            i = 0
            while i < len(self.dupSub):
                tup = self.dupSub[i]
                f = tup[0]
                head = tup[1]
                tail = tup[2] + 1
                if (self.compareList(targetList, self.allList[f][head : tail])):
                    count += 1
                    i += 1
                    tup[2] = tail
                else:
                    del self.dupSub[i]

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

    def writeList(self, ls, file):
        with open(file, "w") as f:
            for key in ls:
                for l in key:
                    f.write(str(l) + "\n")
            f.close()

    '''
    Merge event which is sub array or another event
    '''
    def shrinkResult (self):
        result = self.readByLine(OUTPUT_ID_FILE)
        listCol = []
        for i in range(0, len(result), 2):
            listCol.append(result[i][1:].split(']')[0].split(' '))

        print listCol
        for i in range(len(listCol)):
            if not listCol[i]:
                continue

            for j in range(i + 1, len(listCol)):
                if not listCol[j]:
                    continue
                if (self.isBelongTo(listCol[i], listCol[j])):
                    listCol[i] = []
                elif (self.isBelongTo(listCol[j], listCol[i])):
                    listCol[j] = []
                # print (i, j)

        i = 0
        while i < len(listCol):
            if not listCol[i]:
                del listCol[i]
            else:
                i += 1
        return listCol



    def isBelongTo (self, lista, listb):
        if (len(lista) > len(listb)):
            return False
        else:
            for i in range(0, len(listb) - len(lista) + 1):
                if (self.compareList(lista, listb[i : i + len(lista)])):
                    return True
            return False



    '''
    classify event using union found
    if length of lcs of events is larger than min of len(events), they are unioned.
    output number of classes after classification
    '''

    def classify (self):

        result = self.readByLine("./tmp")
        listCol = []
        for i in range(0, len(result)):
            listCol.append(map(lambda x: x.strip("'"), result[i][1:].split(']')[0].split(', ')))  # my formatter for ./tmp

        print "Number of events: ",
        print len(listCol)
        c = ComSubstr()
        uf = UF(len(listCol))
        for i in range(len(listCol)):
            for j in range(i + 1, len(listCol)):
                # if c.comSubstring(listCol[i], listCol[j]) != 0:
                #     print c.comSubstring(listCol[i], listCol[j])
                # print "vs "
                # print min(len(listCol[i]), len(listCol[j]))
                if (c.comSubstring(listCol[i], listCol[j]) > min(len(listCol[i]), len(listCol[j])) / 2):
                    # print c.comSubstring(listCol[i], listCol[j])
                    uf.union(i, j)

        print "How many classes we have: ",
        print (uf.count())

        '''
        Write classification result to file.
        '''
        r = uf.details()
        with open(CALSSIFY_DETAIL, "w") as f:
            for c in r:
                for id in c:
                    f.write(str(listCol[id]) + "\n")
                f.write("==========" + "\n")
            f.close()



if __name__ == "__main__":
    recurlist = recurList()
    # recurlist.getListAll()
    # print (recurlist.getSize())
    # recurlist.convertToID()


    # recurlist.getListAllFromPickle()
    # print (recurlist.getSize())
    # result = recurlist.recurList()
    # print (result)
    # print (result.values())
    # print (len(result))
    # recurlist.writeResult(result, "./out/recurList_result_id.txt")
    #
    # r = recurlist.shrinkResult()
    # print r
    # print len(r)
    #
    # with open("./tmp", "w") as f:
    #     for i in r:
    #         f.write(str(i) + "\n")
    #     f.close()
    # recurlist.convertFromID(r)   #./out/tmp.out

    recurlist.classify()

    # db = DButil()
    # db.conToDB()
    # result = db.executeCmd("select * from LogTemplateBase")
    # print result
    # print len(result)
    #
    # db.closeCon()




    elapsed = (time.clock() - start)
    print("Time used:", elapsed)
