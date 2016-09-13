# coding: utf8
import tornado.web
from method.method import *

class BaseHandler(tornado.web.RequestHandler):  # 定义一个基础类
    def get_current_user(self):
        return self.get_secure_cookie("username")  # 用于追踪用户的身份


class AdminIndexHandler(BaseHandler):  # 返回首页
    @tornado.web.authenticated
    def get(self):
        user_basename = self.current_user
        self.render('./admin/index.html', user_basename=user_basename)


class UserHandler(BaseHandler):  # 显示用户列表的handler
    @tornado.web.authenticated  # 如果用户没有登录，不允许访问
    def get(self):
        user_basename = self.current_user
        db = self.application.db
        sql = "select * from auth_user;"
        userlist = db.query(sql)
        db.close()
        count = len(userlist)
        one = 0
        self.render('./admin/user.html', userlist=userlist, count=count, one=one, user_basename=user_basename)

    @tornado.web.authenticated
    def post(self):
        user_basename = self.current_user
        data = self.request.arguments
        print data
        user_delete = data.get('_selected_action')
        db = self.application.db
        users = []
        for i in user_delete:
            sql = 'select * from auth_user where id=%s;' % i
            a = db.get(sql)
            users.append(a)
        db.close()
        print users
        # sql = "select * from auth_user;"
        # userlist = db.query(sql)
        # db.close()
        # count = len(userlist)
        self.render('./admin/userdelete.html', users=users, user_basename=user_basename)


class UseraddHandler(BaseHandler):  # 用户添加
    @tornado.web.authenticated
    def get(self):
        user_basename = self.current_user
        passworderr = 0
        username = ''
        useranother = 0
        self.render('./admin/useradd.html', passworderr=passworderr, username=username, useranother=useranother,
                    user_basename=user_basename)

    @tornado.web.authenticated
    def post(self):
        user_basename = self.current_user
        password1 = self.get_argument('password1')
        password2 = self.get_argument('password2')
        username = self.get_argument('username')
        if password1 != password2:
            passworderr = 1
            useranother = 0
            self.render('./admin/useradd.html', passworderr=passworderr, username=username, useranother=useranother,
                        user_basename=user_basename)
        else:
            print password1
            password = password_md5(password1)
            print password
            b = check_password(password, password1)
            print b
            sql = "insert into auth_user (username,password) values ('%s','%s');" % (username, password)
            mysqlinsert(sql)

            data = self.request.arguments
            user_continue = data.get('_continue')
            user_addanother = data.get('_addanother')
            user_save = data.get('_save')
            if user_continue:
                db = self.application.db
                sql = "select * from auth_user where username = '%s';" % username
                userdetail = db.get(sql)
                id = userdetail['id']
                db = self.application.db
                sql = "select * from auth_user where id = %s;" % id
                userdetail = db.get(sql)
                sql = "select * from auth_group;"
                grouplist = db.query(sql)
                print grouplist

                # 处理组的数据
                sql = "select * from auth_user_groups where user_id=%s;" % id
                group = db.query(sql)
                print group
                group_list = []
                for i in group:
                    group_list.append(i['group_id'])

                print group_list

                db.close()
                password_string = 0
                useradd_success = username
                self.render('./admin/userdetail.html', userdetail=userdetail, grouplist=grouplist,
                            group_list=group_list,
                            password_string=password_string, useradd_success=useradd_success,
                            user_basename=user_basename)

            if user_addanother:
                passworderr = 0
                useranother = username
                username = ''
                self.render('./admin/useradd.html', passworderr=passworderr, username=username, useranother=useranother,
                            user_basename=user_basename)

            if user_save:
                self.redirect('/user/')


class UserdetailHandler(BaseHandler):  # 用户的详细信息的handler
    @tornado.web.authenticated
    def get(self, id):  # id 是用户id，用于去数据库里拉取数据
        user_basename = self.current_user
        db = self.application.db
        sql = "select * from auth_user where id = %s;" % id
        userdetail = db.get(sql)
        sql = "select * from auth_group;"
        grouplist = db.query(sql)
        print grouplist

        # 处理组的数据
        sql = "select * from auth_user_groups where user_id=%s;" % id
        group = db.query(sql)
        print group
        group_list = []
        for i in group:
            group_list.append(i['group_id'])

        print group_list

        db.close()
        password_string = 0
        useradd_success = 0
        self.render('./admin/userdetail.html', userdetail=userdetail, grouplist=grouplist, group_list=group_list,
                    password_string=password_string, useradd_success=useradd_success, user_basename=user_basename)

    @tornado.web.authenticated
    def post(self, id):
        user_basename = self.current_user
        data = self.request.arguments
        print data
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        is_staff = data.get('is_staff')
        is_active = data.get('is_active')
        is_superuser = data.get('is_superuser')
        groups = data.get('groups')
        addcontinue = data.get('_continue')
        addanother = data.get('_addanother')
        save = data.get('_save')
        if is_superuser == None:
            is_superuser = 0
        else:
            is_superuser = 1
        if is_staff == None:
            is_staff = 0
        else:
            is_staff = 1
        if is_active == None:
            is_active = 0
        else:
            is_active = 1

        print addanother
        print addcontinue
        print save
        username = username[0]
        first_name = first_name[0]
        last_name = last_name[0]
        email = email[0]
        print groups
        db = self.application.db
        sql = "select * from auth_group;"
        grouplist = db.query(sql)
        sql = "update auth_user set  username='%s',first_name='%s',last_name='%s',email='%s',is_staff=%s,is_active=%s,is_superuser=%s where id = %s;" % (
            username, first_name, last_name, email, is_staff, is_active, is_superuser, id)
        print sql
        db.execute(sql)
        sql = "delete from auth_user_groups where user_id=%s" % id
        db.execute(sql)

        if groups:
            for i in groups:
                sql = "insert into auth_user_groups (user_id,group_id) values (%s,%s);" % (id, i)
                db.execute(sql)

        if addcontinue:
            sql = "select * from auth_user where id = %s;" % id
            userdetail = db.get(sql)

            sql = "select * from auth_user_groups where user_id=%s;" % id
            group = db.query(sql)
            print group
            group_list = []
            for i in group:
                group_list.append(i['group_id'])
            db.close()
            password_string = 0
            useradd_success = username
            self.render('./admin/userdetail.html', userdetail=userdetail, grouplist=grouplist, group_list=group_list,
                        password_string=password_string, useradd_success=useradd_success, user_basename=user_basename)

        if addanother:
            db.close()
            self.redirect('/useradd/')

        if save:
            db.close()
            self.redirect('/user/')


class GroupHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user_basename = self.current_user
        db = self.application.db
        sql = "select * from auth_group;"
        groupdict = db.query(sql)
        count = len(groupdict)
        db.close()
        one = 0
        group_name = 0
        self.render('./admin/group.html', groupdict=groupdict, count=count, one=one, group_name=group_name,
                    user_basename=user_basename)

    @tornado.web.authenticated
    def post(self):
        user_basename = self.current_user
        data = self.request.arguments
        print data
        group_list = data.get('_selected_action')
        print group_list
        groupdelete = []
        db = self.application.db
        for i in group_list:
            sql = 'select * from auth_group where id = %s;' % i
            a = db.get(sql)
            groupdelete.append(a)
        db.close()
        self.render('./admin/groupdelete.html', groupdelete=groupdelete, user_basename=user_basename)


class GroupaddHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        user_basename = self.current_user
        group_addname = 0
        self.render('./admin/groupadd.html', group_addname=group_addname, user_basename=user_basename)

    @tornado.web.authenticated
    def post(self):
        user_basename = self.current_user
        group_name = self.get_argument('name')
        print group_name
        data = self.request.arguments
        group_save = data.get('_save')
        group_addanother = data.get('_addanother')
        group_continue = data.get('_continue')
        db = self.application.db
        sql = "insert into auth_group (name) values ('%s');" % group_name
        db.execute(sql)

        sql = "select * from auth_group where name = '%s';" % group_name
        group = db.get(sql)
        db.close()
        id = group['id']
        url = '/groupdetail/%s' % id

        if group_addanother:
            group_addname = group_name
            print group_addname
            self.render('./admin/groupadd.html', group_addname=group_addname)

        if group_save:
            db = self.application.db
            sql = "select * from auth_group;"
            groupdict = db.query(sql)
            count = len(groupdict)
            db.close()
            one = 0
            print group_name
            self.render('./admin/group.html', groupdict=groupdict, count=count, one=one, group_name=group_name,
                        user_basename=user_basename)

        if group_continue:
            self.redirect(url)


class GroupdetailHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, id):
        user_basename = self.current_user
        db = self.application.db
        sql = "select * from auth_group where id=%s;" % id
        groupdetail = db.get(sql)
        self.render('./admin/groupdetail.html', groupdetail=groupdetail, user_basename=user_basename)


class PasswordHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, id):
        user_basename = self.current_user
        db = self.application.db
        sql = 'select * from  auth_user where id=%s;' % id
        data = db.get(sql)
        print data
        username = data['username']
        db.close()
        alter_string = ''
        self.render('password.html', username=username, id=id, alter_string=alter_string, user_basename=user_basename)

    @tornado.web.authenticated
    def post(self, id):
        user_basename = self.current_user
        password1 = self.get_argument('password1')
        password2 = self.get_argument('password2')
        if password1 == password2:
            password = password_md5(password1)
            print password
            db = self.application.db
            sql = "update auth_user set password='%s' where id=%s;" % (password, id)
            db.execute(sql)
            db.close()

            db = self.application.db
            sql = "select * from auth_user where id = %s;" % id
            userdetail = db.get(sql)
            sql = "select * from auth_group;"
            grouplist = db.query(sql)
            print grouplist

            # 处理组的数据
            sql = "select * from auth_user_groups where user_id=%s;" % id
            group = db.query(sql)
            print group
            group_list = []
            for i in group:
                group_list.append(i['group_id'])

            print group_list
            db.close()
            password_string = 1
            self.render('./admin/userdetail.html', userdetail=userdetail, grouplist=grouplist, group_list=group_list,
                        password_string=password_string, user_basename=user_basename)

        else:
            alter_string = '两次密码输入不一致，请重新输入'
            db = self.application.db
            sql = 'select * from  auth_user where id=%s;' % id
            data = db.get(sql)
            print data
            username = data['username']
            db.close()
            self.render('./admin/password.html', username=username, id=id, alter_string=alter_string,
                        user_basename=user_basename)


class UserdeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        user_basename = self.current_user
        data = self.request.arguments
        users = data.get('_selected_action')
        delete_count = len(users)
        db = self.application.db
        for i in users:
            sql = "delete from auth_user_groups where user_id=%s;" % i
            db.execute(sql)
            sql = "delete from auth_user where id=%s;" % i
            db.execute(sql)

        sql = "select * from auth_user;"
        userlist = db.query(sql)
        db.close()
        count = len(userlist)
        one = delete_count
        self.render('./admin/user.html', userlist=userlist, count=count, one=one, user_basename=user_basename)


class GroupdeleteHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        user_basename = self.current_user
        data = self.request.arguments
        groups = data.get('_selected_action')
        delete_count = len(groups)
        db = self.application.db
        for i in groups:
            sql = "delete from auth_user_groups where group_id=%s;" % i
            db.execute(sql)
            sql = "delete from auth_group where id=%s;" % i
            db.execute(sql)

        sql = "select * from auth_group;"
        groupdict = db.query(sql)
        count = len(groupdict)
        db.close()
        one = delete_count
        group_name = 0
        self.render('./admin/group.html', groupdict=groupdict, count=count, one=one, group_name=group_name,
                    user_basename=user_basename)


class LoginHandler(BaseHandler):
    def get(self):
        error = 0
        self.render('./admin/login.html', error=error, limit=0)

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
                    is_staff = userdata.get('is_staff')
                    print is_active
                    print is_staff
                    if is_staff == 1 and is_active == 1:
                        self.set_secure_cookie("username", self.get_argument("username"))
                        self.redirect("/")
                    else:
                        error = 0
                        limit = 1
                        self.render("./admin/login.html", error=error, limit=limit)
                else:
                    error = 1
                    limit = 0
                    self.render("./admin/login.html", error=error, limit=limit)

            else:
                error = 1
                self.render("./admin/login.html", error=error, limit=0)
        else:
            error = 1
            self.render("./admin/login.html", error=error, limit=0)


class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.clear_cookie("username")
        self.redirect('/login/')
