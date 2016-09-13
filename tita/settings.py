# coding: utf8
import os.path
import torndb
from tornado.options import define, options
from url.urls import *

define("port", default=8090, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="db host")
define("mysql_database", default="tornado", help="db name")
define("mysql_user", default="tornado", help="db user")
define("mysql_password", default="tornado", help="db password")


class Application(tornado.web.Application):
    def __init__(self):
        # url 路由
        handlers = urls


        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "template"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            debug=True,
            # 设置 cookie
            cookie_secret="bZJc2sWbQLKos6GkHn/VB9oXwQt8S0R0kRvJ5/xJ89E=",
            login_url="/login/",  # 默认网页，用户未登陆之前，会自动跳转到此url
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = torndb.Connection(
            host=options.mysql_host,
            database=options.mysql_database,
            user=options.mysql_user,
            password=options.mysql_password
        )  # 将数据库连接做成对象
