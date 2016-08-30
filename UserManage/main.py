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

define("port", default=8080, help="run on the given port", type=int)


class TestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('UserManage/user.add.html')


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", TestHandler),
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
