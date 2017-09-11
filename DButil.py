# export LD_LIBRARY_PATH=/usr/lib/oracle/11.2/client64/lib:$LD_LIBRARY_PATH
import cx_Oracle
CON_STRING = 'sys/cdcora@//etc1m-c2-scan.us.oracle.com:1521/keydb0906.us.oracle.com'

class DButil(object):
    def __init__(self, conString = CON_STRING):
        self.conString = ""

    def conToDB(self, conString = CON_STRING):
        self.conString = conString
        self.conn = cx_Oracle.connect(self.conString,
                                 mode=cx_Oracle.SYSDBA)
        self.myCursor=self.conn.cursor()
        return self.myCursor


        #createTable = "create table LogTemplateBase (LOG_ID NUMBER primary key, LOG_NAME VARCHAR2(30), LOG_TEMP VARCHAR2(300), LOG_TEMP_SCORE NUMBER(38,5), LOG_EXAMPLE VARCHAR2(800), LOG_PRIOPRITY NUMBER, LOG_TYPE VARCHAR2(30))"
        #x = c.execute(createTable)
    def executeCmd(self, cmd):
        x = self.myCursor.execute(cmd)
        self.conn.commit()
        # print self.myCursor.description
        return x.fetchall()

    def queryDesc(self, dbName = "LogTemplateBase"):
        sql = "select * from" + " " + dbName
        x = self.myCursor.execute(sql)
        self.conn.commit()
        print self.myCursor.description
        return self.myCursor.description
    def closeCon(self):
        self.myCursor.close()
        self.conn.close()
    def insertTemps(self, dictList, dbName = "LogTemplateBase"):
        print dictList
        param = dictList
        # tempDict = {}
        # tempDict['LOG_ID'] = 2
        # tempDict['LOG_TEMP'] = 'ABC'
        if dictList:
            # keys = ' values(' + ','.join(map(lambda x: ":" + x, dictList[0].keys())) + ')'
            keys = ' values (:1, :2, :3, :4, :5, :6, :7)'
            values = ' (LOG_ID, LOG_TEMP, LOG_TEMP_SCORE, LOG_PRIORITY, LOG_TYPE, LOG_NAME, LOG_EXAMPLE)'
            print keys
            #self.myCursor.executemany('insert into ' + dbName + ' values(:LOG_NAME,:LOG_ID,:LOG_TEMP_SCORE,:LOG_TEMP,:LOG_EXAMPLE,:LOG_PRIORITY,:LOG_TYPE)', param)
            #self.myCursor.executemany('insert into ' + dbName + keys, param)
            #self.myCursor.executemany('insert into ' + dbName + values + keys, param)
            #self.myCursor.executemany('insert into ' + dbName + ' values(:LOG_TEMP,:LOG_ID)', [tempDict])
            self.myCursor.prepare('insert into ' + dbName + values + keys)
            self.myCursor.executemany(None, dictList)


            self.conn.commit()
        else:
            print "Provide dictList for insertion"
    def dropTable (self, tableName):
        x = self.myCursor.execute("drop table " + tableName)
        self.conn.commit()