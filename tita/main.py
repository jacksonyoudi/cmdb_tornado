import os.path
import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
from settings import *
import method.method
from handler.Admin import *
from handler.CostManager import *





if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
