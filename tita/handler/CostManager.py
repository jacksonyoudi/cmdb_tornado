# coding: utf8
from Admin import BaseHandler
import tornado.web
from method.method import *


class CostlistHandler(BaseHandler):  # 返回成本列表 网页
    @tornado.web.authenticated
    def get(self):
        user_basename = self.get_current_user()
        start, end = month_start_end()
        start1, end1 = lastmonth_start_end()

        sql = 'select e.projectid,e.projectName,e.money,f.money from (select a.projectid,a.projectName,b.money from project_info as a  left join (select * from server_costs where date between %s and %s) as b on  a.projectid = b.projectId) as e left join (select c.projectid,d.money from project_info as c  left join (select * from server_costs where date between %s and %s) as d on  c.projectid = d.projectId) as f  on e.projectid = f.projectid;' % (
            start, end, start1, end1)
        costlist = mysqlselect(sql)  # 获取 列表需要的数据
        # print costlist
        self.render('./costmanager/costlist.html', user_basename=user_basename, costlist=costlist)


class QcloudcostlistHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user_basename = self.get_current_user()
        start, end = lastmonth_start_end()
        sql = 'select id,programe_name,cvm_count,fee from cost_mon_program where mon_date between %s and %s;' % (
            start, end)
        qcloudcostlist = mysqlselect(sql)
        print qcloudcostlist
        self.render('./costmanager/qcloudcostlist.html', user_basename=user_basename, costlist=qcloudcostlist)


class AllviewHandler(BaseHandler):  # 总览的网页
    @tornado.web.authenticated
    def get(self):
        user_basename = self.get_current_user()
        sql = 'select count(projectName) from  qcloud_project;'
        program_count = int(mysqlselect(sql)[0][0])  # 所有项目数
        start, end = month_start_end()
        sql = 'select sum(money) from server_costs where date between %s and %s;' % (start, end)
        month_cost = mysqlselect(sql)[0][0]  # 本月的所有费用

        start, end = lastmonth_start_end()
        sql = 'select sum(money) from server_costs where date between %s and %s;' % (start, end)
        lastmonth_cost = mysqlselect(sql)[0][0]  # 上个月的所有费用

        sql = 'select count(*) from cvm_info;'
        cvm_count = mysqlselect(sql)[0][0]  # 获取cvm的数量

        sql = 'select fee from cost_mon_all where mon_date between %s and %s;' % (start, end)
        qcloud = mysqlselect(sql)[0][0]
        print qcloud
        qcloudcost = '%.2f' % float(qcloud)
        data = qcloud_cost()
        name = '腾讯云每月账单'
        self.render('./costmanager/allview.html', user_basename=user_basename, program_count=program_count,
                    month_cost=month_cost,
                    lastmonth_cost=lastmonth_cost, cvm_count=cvm_count, qcloudcost=qcloudcost, cost=data, name=name)


class ProgramlistHandler(BaseHandler):  # 项目列表的网页
    @tornado.web.authenticated
    def get(self):
        user_basename = self.get_current_user()
        sql = 'select a.projectName,b.cvm_count,a.projectid  from   project_info as a left join  (select projectId,count(*) as cvm_count  from qcloud_cvm group by projectId) as b on a.projectid = b.projectId;'
        program_list = mysqlselect(sql)  # 获取项目列表的数据
        print program_list
        self.render('./costmanager/programlist.html', user_basename=user_basename, program=program_list)


class QcloudBarHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        one = '2016-01-01'
        start, two = lastmonth_start_end()
        projectname = self.get_argument('id')  # 前端网页按钮传递过来的id值，用户锚定项目
        data = project_qcloudcost(one, two, projectname)  # 项目的成本费用数据
        self.render('./costmanager/qcloudbar.html', cost=data,
                    progname=projectname)


class BarHandler(BaseHandler):  # 条形图的handler
    @tornado.web.authenticated
    def get(self):
        user_basename = self.current_user
        name = project_info()  # 所有项目的下拉列表数据
        end = 1000000
        scale = 100000
        one = '2016-01-01'
        two = '2016-09-01'
        projectid = self.get_argument('id')  # 前端网页按钮传递过来的id值，用户锚定项目
        data = project_cost(one, two, projectid)  # 项目的成本费用数据
        t = int(projectid)
        project_name = name[t]  # 项目名
        projectid = t
        print data
        self.render('./costmanager/bar.html', cost=data, projectid=projectid, end=end,
                    scale=scale, one=one, two=two, projectname=name,
                    progname=project_name, user_basename=user_basename)

    @tornado.web.authenticated
    def post(self):  # 提交的处理函数
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
        print project_name
        self.render('./costmanager/bar.html', cost=data, projectid=projectid, end=end,
                    scale=scale, one=one, two=two, projectname=name,
                    progname=project_name, user_basename=user_basename)


class QcloudLineHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        username = self.current_user
        db = self.application.db
        sql = "select * from auth_user where username = '%s';" % username
        user_info = db.get(sql)
        db.close()
        is_superuser = user_info.get('is_superuser')
        one = '2016-01-01'
        start1, two = lastmonth_start_end()
        if is_superuser:  # 判断用户的身份，是否有权限操作
            projectname = self.get_argument('id')

        else:
            group = mysqlgroup(username)
            # id_list = dictkey(group, name)
            # projectid = id_list[0]
            # projectid = int(projectid)
            # project_name = name[projectid]
            # projectname = filter_grouplist(id_list, name)
            projectname = self.get_argument('id')
        name, labels, dataline = qcloudproject_costline(one, two, projectname)  # 绘图需要的数据
        self.render('./costmanager/qcloudline.html',
                    flow=dataline, labels=labels, program=name)


class LineHandler(BaseHandler):  # 曲线图的handler
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
        if is_superuser:  # 判断用户的身份，是否有权限操作
            projectid = int(self.get_argument('id'))
            project_name = name[projectid]
            projectname = name

        else:
            group = mysqlgroup(username)
            id_list = dictkey(group, name)
            projectid = id_list[0]
            projectid = int(projectid)
            project_name = name[projectid]
            projectname = filter_grouplist(id_list, name)
        end = 1000000
        scale = 1000000
        labels, dataline = project_costline(one, two, projectid)  # 绘图需要的数据
        self.render('./costmanager/line.html',
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
        one = self.get_argument('one')  # 开始的时间
        two = self.get_argument('two')  # 结束的时间
        projectid = self.get_argument('three')
        projectid = int(projectid)
        project_name = name[projectid]
        end = 1000000
        scale = 1000000
        if is_superuser:
            projectname = name
        else:
            group = mysqlgroup(username)
            id_list = dictkey(group, name)
            projectname = filter_grouplist(id_list, name)

        labels, dataline = project_costline(one, two, projectid)
        self.render('./costmanager/line.html',
                    flow=dataline, labels=labels, end=end,
                    scale=scale, one=one, two=two, projectname=projectname, program=project_name,
                    projectid=projectid, user_basename=username)


class LineprogramHandler(BaseHandler):  # 普通用户的项目信息handler
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
            project_name = name[projectid]
            projectname = filter_grouplist(id_list, name)
        end = 1000000
        scale = 1000000
        labels, dataline = project_costline(one, two, projectid)
        self.render('./costmanager/lineprogram.html',
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
        self.render('./costmanager/lineprogram.html',
                    flow=dataline, labels=labels, end=end,
                    scale=scale, one=one, two=two, projectname=projectname, program=project_name,
                    projectid=projectid, user_basename=username)


class QcloudtableHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        start, end = month_start_end()
        one = '2016-01-01'
        two = end
        projectname = self.get_argument('id')
        fee = qcloud_costtable(one, two, projectname)

        self.render('./costmanager/qcloudtable.html',
                    dat=fee, program=fee[0][0])


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
            projectid = int(self.get_argument('id'))
            projectname = name
        else:
            group = mysqlgroup(username)
            id_list = dictkey(group, name)
            projectid = id_list[0]
            projectid = int(projectid)
            projectname = filter_grouplist(id_list, name)

        fee = project_costtable(one, two, projectid)
        project_name = name[projectid]

        self.render('./costmanager/table.html',
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
        self.render('./costmanager/table.html',
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
            projectid = int(self.get_argument('id'))
            projectname = name

        else:
            group = mysqlgroup(username)
            id_list = dictkey(group, name)
            projectid = int(id_list[0])
            projectname = filter_grouplist(id_list, name)

        project_name = name[projectid]
        self.render('./costmanager/information.html', projectname=projectname, program=project_name,
                    projectid=projectid)

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
        self.render('./costmanager/information.html', projectname=projectname, program=project_name,
                    projectid=projectid)


class ProgramHandler(BaseHandler):
    @tornado.web.authenticated
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
        # groupname = int(projectid)
        data = project_cost(one, two, projectid)
        print data
        self.render('./costmanager/program.html', cost=data, user_basename=user_basename, program=group, one=one,
                    two=two,
                    projectname=projectname, groupname=groupname, projectid=projectid)

    @tornado.web.authenticated
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
        # groupname = int(projectid)
        data = project_cost(one, two, projectid)
        print data
        self.render('./costmanager/program.html', cost=data, user_basename=user_basename, program=group, one=one,
                    two=two,
                    projectname=projectname, groupname=groupname, projectid=projectid)


class QcloudUserHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user_basename = self.current_user
        name = project_info()
        group = mysqlgroup(user_basename)
        id_list = dictkey(group, name)
        projectname = filter_grouplist(id_list, name)

        start, two = lastmonth_start_end()
        li = []
        for k, v in projectname.items():
            li.append(v)
        st = '('
        for i in range(len(li)):
            if i == len(li) - 1:
                st = st + "'" + str(li[i]) + "'"
            else:
                st = st + "'" + str(li[i]) + "'" + ','
        st = st + ')'
        print st
        sql = 'select id,programe_name,cvm_count,fee from cost_mon_program where programe_name in %s and mon_date between %s and %s;' % (
            st, start, two)
        data = mysqlselect(sql)
        self.render('./costmanager/qclouduserlist.html', costlist=data, user_basename=user_basename)


class LoginHandler(BaseHandler):
    def get(self):
        error = 0
        self.render('./costmanager/login.html', error=error, limit=0)

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
                            self.redirect("/allview/")
                        else:
                            self.redirect("/program/")
                    else:
                        error = 0
                        limit = 1
                        self.render("./costmanager/login.html", error=error, limit=limit)
                else:
                    error = 1
                    limit = 0
                    self.render("./costmanager/login.html", error=error, limit=limit)

            else:
                error = 1
                self.render("./costmanager/login.html", error=error, limit=0)
        else:
            error = 1
            self.render("./costmanager/login.html", error=error, limit=0)


class UserChangePasswordHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        db = self.application.db
        user_basename = self.current_user
        username = user_basename
        sql = "select id,username from auth_user where username='%s'" % username
        user = db.get(sql)
        id = user['id']
        alter_string = ''
        self.render('./costmanager/userpassword.html', username=username, id=id, alter_string=alter_string,
                    user_basename=user_basename)

    @tornado.web.authenticated
    def post(self, id):
        user_basename = self.current_user
        username = user_basename
        password1 = self.get_argument('password1')
        password2 = self.get_argument('password2')
        if password1 == password2:
            password = password_md5(password1)

            db = self.application.db
            sql = "update auth_user set password='%s' where id=%s;" % (password, id)
            db.execute(sql)
            db.close()
            alter_string = '密码修改成功'
            self.render('./costmanager/userpassword.html', username=username, id=id, alter_string=alter_string,
                        user_basename=user_basename)

        else:
            alter_string = '两次密码输入不一致，请重新输入'
            db = self.application.db
            sql = 'select * from  auth_user where id=%s;' % id
            data = db.get(sql)
            print data
            username = data['username']
            db.close()
            self.render('./costmanager/userpassword.html', username=username, id=id, alter_string=alter_string,
                        user_basename=user_basename)
