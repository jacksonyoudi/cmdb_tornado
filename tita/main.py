# coding: utf8
import os.path
import tornado.web
import tornado.ioloop
import tornado.httpserver
# import tornado.options
from tornado.options import define, options

# from settings import Application
import method.method
from handler.Admin import *
from handler.CostManager import *
from url.urls import urls
import torndb


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



if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
