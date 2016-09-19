#!/usr/bin/env python
# coding: utf8

import xlrd
import sys
import MySQLdb
import datetime

cmdb_host = "localhost"
cmdb_user = "ledou"
cmdb_db = "ledou_cmdb"
cmdb_port = 3306
cmdb_passwd = "ledou"

cmdb_db = {"host": cmdb_host, 'user': cmdb_user, 'db': cmdb_db, 'passwd': cmdb_passwd, 'port': cmdb_port}

conn = MySQLdb.connect(db=cmdb_db['db'], host=cmdb_db['host'], user=cmdb_db['user'], passwd=cmdb_db['passwd'],
                       port=cmdb_db['port'])

cur = conn.cursor()

reload(sys)
sys.setdefaultencoding('utf8')

try:
    def date_gen(mon):
        if len(mon) == 1:
            mon = '0' + mon
        d = datetime.datetime.now()
        year = str(d.year)
        date_str = '%s%s%s' % (year, mon, '15')
        return date_str


    sheet_list = [2, 4, 6, 8, 10, 12, 14, 16]

    # xlsx

    workbook = xlrd.open_workbook('1.xlsx')

    for i in sheet_list:
        sheet = workbook.sheets()[i]
        name = sheet.name
        mon = name.split('月')[0]
        date_str = date_gen(mon)

        rows = sheet.nrows
        print rows
        c = sheet.row_values(rows - 1)[0].encode('utf8').split('：')[1]
        print type(c)
        all = float(str(c))
        sql = 'insert into cost_mon_all (fee,mon_date) values (%s,%s);' % (all, date_str)
        cur.excute(sql)

        for j in xrange(rows - 1):
            cost_list = []
            cost_list.append(sheet.row_values(j)[0].encode('utf8'))
            cost_list.append(int(sheet.row_values(j)[1]))
            cost_list.append(sheet.row_values(j)[2])
            cost_list.append(date_str)

            sql = 'insert into cost_mon_program (program_name,cvm_count,fee,mon_date) values (%s,%s,%s,%s);' % (
                cost_list[0], cost_list[1], cost_list[2], cost_list[3])
            cur.excute(sql)

    cur.close()
    conn.commit()
except Exception, e:
    print e
    conn.rollback()
finally:
    conn.close()
