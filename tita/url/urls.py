# coding: utf8
from handler.Admin import AdminIndexHandler, UserHandler, PasswordHandler, UseraddHandler, UserdetailHandler, \
    GroupHandler, GroupdeleteHandler, UserdeleteHandler, GroupaddHandler, GroupdetailHandler,LogoutHandler
from handler.CostManager import LoginHandler, BarHandler, LineHandler, LineprogramHandler, TableHandler, \
    InformationHandler, ProgramHandler, AllviewHandler, ProgramlistHandler, CostlistHandler, UserChangePasswordHandler

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
    (r"/userchangepassword/", UserChangePasswordHandler),
    (r"/userchangepassword/([0-9]+)", UserChangePasswordHandler),
    # (r"/ip/", IpHandler),
]
