#!/usr/bin/env python
# coding: utf8

import os.path
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import MySQLdb
from MySQLdb.constants import FIELD_TYPE
import json
import sys

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)


def mysqlselect(sql):
    my_conv = {FIELD_TYPE.TIMESTAMP: str}
    conn = MySQLdb.connect(host="localhost", user="ledou", passwd="ledou", db="ledou_cmdb", port=3306,
                           conv=my_conv)
    cur = conn.cursor()
    cur.execute('set names utf8')
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


def project_info():
    conn = MySQLdb.connect(host="localhost", user="ledou", passwd="ledou", db="ledou_cmdb", port=3306, charset='utf8')
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


def project_cost(on, tw, projectid):
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


def project_costline(on, tw, projectid):
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


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('test.html')


class AllHandler(tornado.web.RequestHandler):
    def get(self):
        name = project_info()
        end = 1000000
        scale = 100000
        username = 'root'
        one = '2016-01-01'
        two = '2016-09-01'
        projectid = '1000330'
        data = project_cost(one, two, projectid)
        t = int(projectid)
        project_name = name[t]
        projectid = t
        self.render('all.html', cost=data, projectid=projectid, end=end,
                    scale=scale, username=username, one=one, two=two, projectname=name,
                    progname=json.dumps(project_name))

    def post(self):
        name = project_info()
        end = 1000000
        scale = 100000
        username = 'root'
        one = self.get_argument('one')
        two = self.get_argument('two')
        projectid = self.get_argument('three')
        data = project_cost(one, two, projectid)
        t = int(projectid)
        project_name = name[t]
        projectid = t
        self.render('all.html', cost=data, projectid=projectid, end=end,
                    scale=scale, username=username, one=one, two=two, projectname=name,
                    progname=json.dumps(project_name))


class LineHandler(tornado.web.RequestHandler):
    def get(self):
        name = project_info()
        one = '2016-01-01'
        two = '2016-09-01'
        projectid = 1000330
        project_name = projectid
        labels, dataline = project_costline(one, two, projectid)
        projectname = name
        end = 1000000
        scale = 1000000
        self.render('line.html',
                    flow=dataline, labels=labels, end=end,
                    scale=scale, one=one, two=two, projectname=projectname, program=project_name,
                    projectid=projectid)

    def post(self):
        name = project_info()
        one = self.get_argument('one')
        two = self.get_argument('two')
        projectid = self.get_argument('three')
        projectid = int(projectid)
        project_name = projectid
        labels, dataline = project_costline(one, two, projectid)
        projectname = name
        end = 1000000
        scale = 1000000
        self.render('line.html',
                    flow=dataline, labels=labels, end=end,
                    scale=scale, one=one, two=two, projectname=projectname, program=project_name,
                    projectid=projectid)


class TableHandler(tornado.web.RequestHandler):
    def get(self):
        name = project_info()
        one = '2016-01-01'
        two = '2016-09-01'
        projectid = 1000330
        fee = project_costtable(one, two, projectid)
        project_name = name[projectid]
        projectname = name
        print fee
        self.render('table.html',
                    dat=fee, program=project_name, one=one, two=two, projectid=projectid,
                    projectname=projectname)

    def post(self):
        name = project_info()
        one = self.get_argument('one')
        two = self.get_argument('two')
        projectid = self.get_argument('three')
        fee = project_costtable(one, two, projectid)
        projectid = int(projectid)
        project_name = name[projectid]
        projectname = name
        self.render('table.html',
                    dat=fee, program=project_name, one=one, two=two, projectid=projectid,
                    projectname=projectname)


class InformationHandler(tornado.web.RequestHandler):
    def get(self):
        


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", AllHandler),
            (r"/update/", AllHandler),
            (r"/line/", LineHandler),
            (r"/table/", TableHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "template"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
