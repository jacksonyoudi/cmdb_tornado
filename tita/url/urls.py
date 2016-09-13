# coding: utf8
from handler.Admin import *
from handler.CostManager import *

urls = [
    (r"/", LoginHandler),
    (r"/admin/", AdminIndexHandler),
    (r"/user/", UserHandler),
    (r"/password/([0-9]+)", PasswordHandler),
    (r"/useradd/", UseraddHandler),
    (r"/userdetail/([0-9]+)", UserdetailHandler),
    (r"/group/", GroupHandler),
    (r"/groupdelete/", GroupdeleteHandler),
    (r"/userdelete/", UserdeleteHandler),
    (r"/groupadd/", GroupaddHandler),
    (r"/login/", LoginHandler),
    (r"/logout/", LogoutHandler),
    # (r"/back/", BackHandler),
    (r"/groupdetail/([0-9]+)", GroupdetailHandler),
    (r"/bar/", BarHandler),
    (r"/line/", LineHandler),
    (r"/lineprogram/", LineprogramHandler),
    (r"/table/", TableHandler),
    (r"/information/", InformationHandler),
    (r"/program/", ProgramHandler),
    (r"/allview/", AllviewHandler),
    (r"/programlist/", ProgramlistHandler),
    (r"/costlist/", CostlistHandler),
    # (r"/ip/", IpHandler),
]
