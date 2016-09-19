#!/usr/bin/env python
# coding: utf8


import MySQLdb
from MySQLdb.constants import FIELD_TYPE
import sys
import calendar
import time
import os

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from settings import cmdb_db, admin_db


# import sett

def mysqlinsert(sql):  # 定义插入数据库的函数,由于使用torndb出现异常，故改用mysqldb
    try:
        conn = MySQLdb.connect(db=admin_db['db'], host=admin_db['host'], user=admin_db['user'],
                               passwd=admin_db['passwd'], port=admin_db['port'])
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.commit()
        conn.close()
    except Exception, e:
        print "error"
        print e


def password_md5(password_string):  # 生成密码MD5校验
    string = 'openssl passwd -1 %s' % password_string
    output = os.popen(string)
    result = output.read()
    result = result.replace('\n', '')
    return result


def check_password(password_string, password):  # 对密码进行校验，参数为数据库密码和用户输入的密码
    salt = password_string.split('$')[2]
    string = 'openssl passwd -1 -salt %s   %s' % (salt, password)
    output = os.popen(string)
    result = output.read()
    result = result.replace('\n', '')
    return result


def mysqlselect(sql):  # 定义查询的mysql数据方法，参数就是sql语句
    my_conv = {FIELD_TYPE.TIMESTAMP: str}
    conn = MySQLdb.connect(db=cmdb_db['db'], host=cmdb_db['host'], user=cmdb_db['user'], passwd=cmdb_db['passwd'],
                           port=cmdb_db['port'],
                           conv=my_conv)
    cur = conn.cursor()
    cur.execute('set names utf8')
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


def project_info():  # 查询 project_info信息的函数
    conn = MySQLdb.connect(db=cmdb_db['db'], host=cmdb_db['host'], user=cmdb_db['user'], passwd=cmdb_db['passwd'],
                           port=cmdb_db['port'], charset='utf8')
    cur = conn.cursor()
    sql = 'select projectid,projectName from project_info;'
    cur.execute('set names utf8')
    cur.execute(sql)
    name = cur.fetchall()
    cur.close()
    conn.close()
    data = []
    for i in name:
        d = []
        d.append(int(i[0]))
        d.append(i[1])
        data.append(d)
    project_dict = []
    for i in data:
        project_dict.append(tuple(i))
    name = dict(project_dict)
    return name


def project_cost(on, tw, projectid):  # 查询project_cost的函数
    one = on.replace('-', '', 2)
    two = tw.replace('-', '', 2)
    sql = 'select date,money from server_costs where date between "%s" and "%s" and projectId = %s;' % (
        one, two, projectid)
    t = mysqlselect(sql)
    d = []
    l = []
    for i in t:
        d.append(str(i[0]))
        l.append(int(i[1]))
    b = []
    for i in range(20):
        b.append('#32bdbc')

    z = zip(d, l, b)

    a = []
    for i in z:
        a.append({'name': i[0], 'value': int(i[1]), 'color': i[2]})

    return a


def qcloud_cost():
    sql = 'select mon_date,fee from cost_mon_all;'
    t = mysqlselect(sql)
    d = []
    l = []
    for i in t:
        d.append(str(i[0]))
        l.append(float(i[1]))
    b = []
    for i in range(20):
        b.append('#32bdbc')

    z = zip(d, l, b)

    a = []
    for i in z:
        a.append({'name': i[0], 'value': i[1], 'color': i[2]})
    return a


def project_costline(on, tw, projectid):  # 返回值是传递给曲线图的参数
    one = on.replace('-', '', 2)
    two = tw.replace('-', '', 2)
    sql = 'select date,money from server_costs where date between "%s" and "%s" and projectId = %s;' % (
        one, two, projectid)
    t = mysqlselect(sql)
    d = []
    l = []
    for i in t:
        d.append(str(i[0]))
        l.append(int(i[1]))

    return d, l


def project_costtable(on, tw, projectid):
    one = on.replace('-', '', 2)
    two = tw.replace('-', '', 2)
    sql = 'select date,money from server_costs where date between "%s" and "%s" and projectId = %s;' % (
        one, two, projectid)
    t = mysqlselect(sql)
    d = []
    l = []
    for i in t:
        d.append(str(i[0]))
        l.append(int(i[1]))
    b = []
    for i in range(20):
        b.append('#32bdbc')

    z = zip(d, l, b)
    print z

    a = []
    for i in z:
        a.append({'name': i[0], 'value': int(i[1]), 'color': i[2]})

    return a


def mysqlgroup(username):  # 获取用户组的数据
    try:
        c = MySQLdb.connect(db=admin_db['db'], host=admin_db['host'], user=admin_db['user'],
                            passwd=admin_db['passwd'], port=admin_db['port'], charset='utf8')
        cur = c.cursor()
        sql = "select  d.name from auth_group as d,(select a.group_id from auth_user_groups as a,(select id from auth_user where username = '%s') as b where a.user_id = b.id) as c where d.id = c.group_id ; " % username
        cur.execute(sql)
        t = cur.fetchall()
        cur.close()
        c.close()
        a = []
        for i in t:
            a.append(i[0])
        return a
    except Exception, e:
        print e


def dictkey(i, d):
    a = []
    for j in i:
        for k, v in d.items():
            if v == j:
                a.append(k)
    return a


def filter_grouplist(l, d):
    a = {}
    for i in l:
        a[i] = d[i]
    return a


def month_start_end():  # 获取当前  月初和月末的时间
    day_now = time.localtime()
    day_begin = '%d%02d01' % (day_now.tm_year, day_now.tm_mon)
    wday, monthRange = calendar.monthrange(day_now.tm_year, day_now.tm_mon)
    day_end = '%d%02d%02d' % (day_now.tm_year, day_now.tm_mon, monthRange)
    return day_begin, day_end


def lastmonth_start_end():  # 获取上个月的 月初和月末
    import datetime
    d = datetime.datetime.now()
    days_count = datetime.timedelta(days=d.day)
    last_month = d - days_count
    day_start = datetime.datetime(last_month.year, last_month.month, 1, 0, 0, 0)
    day_end = datetime.datetime(last_month.year, last_month.month, last_month.day, 23, 59, 59)
    month_start = '%d%02d01' % (day_start.year, day_start.month)
    month_end = '%d%02d%02d' % (day_end.year, day_end.month, day_end.day)
    return month_start, month_end
