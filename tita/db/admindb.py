# coding: utf8
import tornado.web
import torndb


tornado.web.Application.__init__(self, handlers, **settings)
self.db = torndb.Connection(
    host=options.mysql_host,
    database=options.mysql_database,
    user=options.mysql_user,
    password=options.mysql_password
)  # 将数据库连接做成对象
