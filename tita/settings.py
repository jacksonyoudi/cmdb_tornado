# coding: utf8
import os.path
from tornado.options import define, options

# 定义数据库参数
# cmdb
cmdb_host = "localhost"
cmdb_user = "ledou"
cmdb_db = "ledou_cmdb"
cmdb_port = 3306
cmdb_passwd = "ledou"

# admin
admin_host = "localhost"
admin_user = "tornado"
admin_db = "tornado"
admin_port = 3306
admin_passwd = "tornado"

cmdb_db = {"host": cmdb_host, 'user': cmdb_user, 'db':cmdb_db, 'passwd': cmdb_passwd, 'port': cmdb_port}
admin_db = {"host": admin_host, 'user': admin_user, 'db': admin_db, 'passwd': admin_passwd, 'port': admin_port}

define("port", default=8090, help="run on the given port", type=int)
define("mysql_host", default="127.0.0.1:3306", help="db host")
define("mysql_database", default="tornado", help="db name")
define("mysql_user", default="tornado", help="db user")
define("mysql_password", default="tornado", help="db password")


