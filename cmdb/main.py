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
import tornado.httpserver
import torndb

from tornado.options import define, options

define("port", default=8090, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="db host")
define("mysql_database", default="tornado", help="db name")
define("mysql_user", default="tornado", help="db user")
define("mysql_password", default="tornado", help="db password")


def check_password(password_string, password):
    salt = password_string.split('$')[2]
    string = 'openssl passwd -1 -salt %s   %s' % (salt, password)
    output = os.popen(string)
    result = output.read()
    result = result.replace('\n', '')
    return result


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", AllHandler),
            (r"/update/", AllHandler),
            (r"/line/", LineHandler),
            (r"/table/", TableHandler),
            (r"/information/", InformationHandler),
            (r"/login/", LoginHandler),
            (r"/logout/", LogoutHandler),
            (r"/program/", ProgramHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "template"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
            cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            login_url="/login/",
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = torndb.Connection(
            host=options.mysql_host,
            database=options.mysql_database,
            user=options.mysql_user,
            password=options.mysql_password
        )


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


def mysqlgroup(username):
    try:
        c = MySQLdb.connect(host='localhost', user='tornado', passwd='tornado', db='tornado', port=3306, charset='utf8')
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


class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")


class IndexHandler(BaseHandler):
    def get(self):
        self.render('test.html')


class AllHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user_basename = self.current_user
        name = project_info()
        end = 1000000
        scale = 100000
        one = '2016-01-01'
        two = '2016-09-01'
        projectid = '1000363'
        data = project_cost(one, two, projectid)
        t = int(projectid)
        project_name = name[t]
        projectid = t
        print data
        self.render('all.html', cost=data, projectid=projectid, end=end,
                    scale=scale, one=one, two=two, projectname=name,
                    progname=json.dumps(project_name), user_basename=user_basename)

    @tornado.web.authenticated
    def post(self):
        user_basename = self.current_user
        name = project_info()
        end = 1000000
        scale = 100000
        one = self.get_argument('one')
        two = self.get_argument('two')
        projectid = self.get_argument('three')
        data = project_cost(one, two, projectid)
        t = int(projectid)
        project_name = name[t]
        projectid = t
        print data
        self.render('all.html', cost=data, projectid=projectid, end=end,
                    scale=scale, one=one, two=two, projectname=name,
                    progname=json.dumps(project_name), user_basename=user_basename)


class LineHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        username = self.current_user
        db = self.application.db
        sql = "select * from auth_user where username = '%s';" % username
        user_info = db.get(sql)
        db.close()
        is_superuser = user_info.get('is_superuser')
        name = project_info()
        one = '2016-01-01'
        two = '2016-09-01'
        if is_superuser:
            projectid = 1000363
            project_name = projectid
            projectname = name

        else:
            group = mysqlgroup(username)
            id_list = dictkey(group, name)
            projectid = id_list[0]
            projectid = int(projectid)
            project_name = projectid
            projectname = filter_grouplist(id_list, name)
        end = 1000000
        scale = 1000000
        labels, dataline = project_costline(one, two, projectid)
        self.render('lineall.html',
                    flow=dataline, labels=labels, end=end,
                    scale=scale, one=one, two=two, projectname=projectname, program=project_name,
                    projectid=projectid, user_basename=username)

    @tornado.web.authenticated
    def post(self):
        username = self.current_user
        db = self.application.db
        sql = "select * from auth_user where username = '%s';" % username
        user_info = db.get(sql)
        db.close()
        is_superuser = user_info.get('is_superuser')
        name = project_info()
        one = self.get_argument('one')
        two = self.get_argument('two')
        projectid = self.get_argument('three')
        projectid = int(projectid)
        project_name = projectid
        end = 1000000
        scale = 1000000
        if is_superuser:
            projectname = name
        else:
            group = mysqlgroup(username)
            id_list = dictkey(group, name)
            projectname = filter_grouplist(id_list, name)

        labels, dataline = project_costline(one, two, projectid)
        self.render('line.html',
                    flow=dataline, labels=labels, end=end,
                    scale=scale, one=one, two=two, projectname=projectname, program=project_name,
                    projectid=projectid)


class TableHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        username = self.current_user
        db = self.application.db
        sql = "select * from auth_user where username = '%s';" % username
        user_info = db.get(sql)
        db.close()
        is_superuser = user_info.get('is_superuser')
        name = project_info()
        one = '2016-01-01'
        two = '2016-09-01'
        if is_superuser:
            projectid = 1000363
            projectname = name
        else:
            group = mysqlgroup(username)
            id_list = dictkey(group, name)
            projectid = id_list[0]
            projectid = int(projectid)
            projectname = filter_grouplist(id_list, name)

        fee = project_costtable(one, two, projectid)
        project_name = name[projectid]

        self.render('table.html',
                    dat=fee, program=project_name, one=one, two=two, projectid=projectid,
                    projectname=projectname)

    @tornado.web.authenticated
    def post(self):
        username = self.current_user
        db = self.application.db
        sql = "select * from auth_user where username = '%s';" % username
        user_info = db.get(sql)
        db.close()
        is_superuser = user_info.get('is_superuser')
        name = project_info()
        one = self.get_argument('one')
        two = self.get_argument('two')
        projectid = self.get_argument('three')
        fee = project_costtable(one, two, projectid)
        projectid = int(projectid)
        project_name = name[projectid]
        if is_superuser:
            projectname = name
        else:
            group = mysqlgroup(username)
            id_list = dictkey(group, name)
            projectname = filter_grouplist(id_list, name)
        self.render('table.html',
                    dat=fee, program=project_name, one=one, two=two, projectid=projectid,
                    projectname=projectname)


class InformationHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        username = self.current_user
        db = self.application.db
        sql = "select * from auth_user where username = '%s';" % username
        user_info = db.get(sql)
        db.close()
        is_superuser = user_info.get('is_superuser')
        name = project_info()
        if is_superuser:
            projectid = 1000363
            projectname = name

        else:
            group = mysqlgroup(username)
            id_list = dictkey(group, name)
            projectid = int(id_list[0])
            projectname = filter_grouplist(id_list, name)

        project_name = name[projectid]
        self.render('information.html', projectname=projectname, program=project_name, projectid=projectid)

    @tornado.web.authenticated
    def post(self):
        username = self.current_user
        db = self.application.db
        sql = "select * from auth_user where username = '%s';" % username
        user_info = db.get(sql)
        db.close()
        is_superuser = user_info.get('is_superuser')
        name = project_info()
        projectid = self.get_argument('three')
        projectid = int(projectid)

        project_name = name[projectid]
        if is_superuser:
            projectname = name
        else:
            group = mysqlgroup(username)
            id_list = dictkey(group, name)
            projectname = filter_grouplist(id_list, name)
        self.render('information.html', projectname=projectname, program=project_name, projectid=projectid)


class ProgramHandler(BaseHandler):
    def get(self):
        user_basename = self.current_user
        name = project_info()
        group = mysqlgroup(user_basename)
        id_list = dictkey(group, name)
        projectname = filter_grouplist(id_list, name)
        one = '2016-01-01'
        two = '2016-09-01'
        projectid = id_list[0]
        projectid = int(projectid)
        groupname = name[int(projectid)]
        data = project_cost(one, two, projectid)
        print data
        self.render('program.html', cost=data, user_basename=user_basename, program=group, one=one, two=two,
                    projectname=projectname, groupname=json.dumps(groupname), projectid=projectid)

    def post(self):
        user_basename = self.current_user
        name = project_info()
        group = mysqlgroup(user_basename)
        id_list = dictkey(group, name)
        projectname = filter_grouplist(id_list, name)
        one = self.get_argument('one')
        two = self.get_argument('two')
        projectid = self.get_argument('three')
        projectid = int(projectid)
        groupname = name[int(projectid)]
        data = project_cost(one, two, projectid)
        print data
        self.render('program.html', cost=data, user_basename=user_basename, program=group, one=one, two=two,
                    projectname=projectname, groupname=json.dumps(groupname), projectid=projectid)


class LoginHandler(BaseHandler):
    def get(self):
        error = 0
        self.render('login.html', error=error, limit=0)

    def post(self):
        data = self.request.arguments
        username = data.get('username')
        password = data.get('password')
        if username and password:
            username = self.get_argument('username')
            password = self.get_argument('password')
            db = self.application.db
            sql = "select * from auth_user where username = '%s';" % username
            userdata = db.get(sql)
            db.close()
            if userdata:
                password_db = userdata['password']
                password_input = check_password(password_db, password)

                if password_input == password_db:
                    is_active = userdata.get('is_active')
                    is_superuser = userdata.get('is_superuser')
                    print is_active
                    if is_active == 1:
                        self.set_secure_cookie("username", self.get_argument("username"))
                        if is_superuser:
                            self.redirect("/")
                        else:
                            self.redirect("/program/")
                    else:
                        error = 0
                        limit = 1
                        self.render("login.html", error=error, limit=limit)
                else:
                    error = 1
                    limit = 0
                    self.render("login.html", error=error, limit=limit)

            else:
                error = 1
                self.render("login.html", error=error, limit=0)
        else:
            error = 1
            self.render("login.html", error=error, limit=0)


class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.clear_cookie("username")
        self.redirect('/login/')


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
