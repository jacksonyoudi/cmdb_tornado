# coding: utf8
from Admin import BaseHandler
import tornado.web
from method.servermethod import LoginVirifi
import time
import yaml


class ServerinitHandler(BaseHandler):
    def get(self):
        user_basename = self.get_current_user()
        self.render('./server/serverinit.html', user_basename=user_basename)

    def post(self):
        user_basename = self.get_current_user()
        PACKAGE = self.get_argument('package')  # 获取前端提交的数据
        PACKAGE_LINE = [i.split() for i in PACKAGE.encode('utf-8').split('\r\n')]  # 把多行数据按行转换成列表，每个元素都是列表
        # logger.debug('%s, PACKAGE_LINE: %s', username, PACKAGE_LINE)
        SALTCMD = 'Host Initialization'
        SALT_FUN = 'host.init'

        ecount = 0
        SALTRET = []
        SALTRET.append('')
        ## 需要加入主机名和IP地址不重复验证
        ## 日后再加
        for ELMENT in PACKAGE_LINE:  # [['192.68.172.11', 'net'],['192.68.172.12', 'game']] 格式
            j = ' '.join(ELMENT)  # 转换成 '192.68.172.11 net'格式
            if len(ELMENT) < 2:  # 小于两个元素，
                ecount += 1
                SALTRET.append({j: 1})  # [{'192.68.172.11'}:1,]
            else:
                SALTRET.append({j: 0})  # [{''}:0,]
        # logger.debug('%s, ecount: %s SALTRET: %s', username, ecount, SALTRET)
        if ecount > 0:
            SALTRET[0] = '下列标红的行所提供之信息不完整，请修正后重新提交: '
            self.render('result.html', SALTCOMMAND=SALTCMD, ECOUNT=ecount, SALTRESULT=SALTRET, FLAGID=id,
                        MENUDICT=menudict, SALTFUNCTION=SALT_FUN, PERMISSION=permission)

        else:
            ret_usertype = 0
            PACKAGE_DICT = {}
            HOSTNAME_DICT = {}
            ROSTER_CONF = '.roster_' + str(time.time())  # .roster_1473837713.844112
            for USER in ['root', 'ubuntu']:
                if USER == 'root':
                    for ELMENT in PACKAGE_LINE:
                        if len(ELMENT) == 3:  # 3个元素，ip name password
                            PASS = ELMENT[-1]  # 取密码
                        else:
                            PASS = '1234Qwer'  # 否则，默认密码
                        PACKAGE_DICT[ELMENT[1]] = {'host': ELMENT[0], 'user': USER, 'passwd': PASS, 'port': 22}
                        # PACKAGE_DICT={'game':{'host': '192.168.1.9', 'user': 'root', 'passwd': 'pasword', 'port': 22},}
                        HOSTNAME_DICT[ELMENT[0]] = ELMENT[1]
                        # HOSTNAME_DICT = {'192.168.1.4':'game'}
                        PACKAGE_YAML = yaml.dump(PACKAGE_DICT)
                        # 字典转化为yaml格式
                        # logger.debug('%s, PACKAGE_YAML: %s', username, PACKAGE_YAML)
                        ROSTER_FD = open(ROSTER_CONF, 'w')
                        # .roster_1473837713.844112 创建文件
                        ROSTER_FD.write(PACKAGE_YAML)
                        # 写入 yaml 格式文件
                        ROSTER_FD.close()
                        # 关闭
                elif USER == 'ubuntu':
                    # retb = LoginVirifi(PACKAGE_DICT)
                    for hosty in retb:  # SALTRET
                        if retb[hosty] == 0:
                            PACKAGE_DICT.pop(hosty)
                        elif retb[hosty] == 1:
                            PACKAGE_DICT[hosty]['user'] = 'ubuntu'
                            # 字典  {'192.168.1.1':{'user':'ubuntu'},}

                # logger.debug('%s, PACKAGE_DICT: %s', username, PACKAGE_DICT)
                TARGET = ','.join([i for i in HOSTNAME_DICT.values()])

                ## 验证ssh的用户密码是否正确
                SALTSSH_RETFILE = '.saltsshret_' + str(time.time())
                # '.saltsshret_1473837713.844112'

                retb = LoginVirifi(PACKAGE_DICT)
                # logger.debug('%s, The result of LoginVirifi: %s', username, retb)
                retc = sum(retb.values())
                if retc == 0:
                    ret_usertype = ret_usertype - 1
                    # logger.debug('%s, All host LoginVirifi success,ret_usertype: %s', username, ret_usertype)
                    break
                else:
                    ret_usertype = 1
                    # logger.debug('%s, All or part of host LoginVirifi fail,ret_usertype: %s', username,
                    #              ret_usertype)
                    continue

            ## 验证用户为ubuntu时，修改root密码与ubuntu用户密码相同
            ## ubuntu 用户修改root 密码失败暂未做处理
            if ret_usertype == 1:
                ecount = -1
                SALTRET = []
                SALTRET.append('下列标红的服务器ssh登录失败，请修正后重新提交：')
                for j in PACKAGE_LINE:
                    k = ' '.join(j)
                    if j[1] in retb.keys():
                        SALTRET.append({k: 1})
                    else:
                        SALTRET.append({k: 0})
                # logger.info('%s, ecount: %s SALTRET: %s', username, ecount, SALTRET)
                self.render('./server/result.html', SALTCOMMAND=SALTCMD, ECOUNT=ecount, SALTRESULT=SALTRET, FLAGID=id,
                             SALTFUNCTION=SALT_FUN,user_basename=user_basename)
            else:
                # SALT_FUN = 'state.sls'
                self.render('./server/result.html', SALTCOMMAND=SALTCMD, ECOUNT=ecount, SALTRESULT=SALTRET, FLAGID=id,
                             SALTFUNCTION=SALT_FUN,user_basename=user_basename)

                ## 验证用户为ubuntu时，修改root密码与ubuntu用户密码相同
                ## ubuntu 用户修改root 密码失败暂未做处理
                if ret_usertype == 0:
                    retd = ChangePasswd(PACKAGE_DICT)
                    # logger.debug('%s, The result of ChangePasswd: %s', username, retd)
                    rete = sum(retd.values())

                ## host init
                client = SSHClient()
                # logger.debug(
                #     "%s, client.cmd\(tgt=%s,fun='state.sls', arg=['inithost'],roster_file=%s,expr_form=\'list\',kwarg={'pillar':%s,}\)",
                #     username, TARGET, ROSTER_CONF, HOSTNAME_DICT)
                # rand_thin_dir=True or -W is for fixing the salt-ssh problem when minion is python2.7 and master is python2.6 can cause error below:
                # 'AttributeError: 'module' object has no attribute 'fromstringlist
                # refer https://github.com/saltstack/salt/issues/26584
                RET = client.cmd(tgt=TARGET, fun='state.sls', arg=['inithost'], roster_file=ROSTER_CONF,
                                 expr_form='list', ignore_host_keys=True, rand_thin_dir=True,
                                 kwarg={'pillar': HOSTNAME_DICT})
                # logger.debug('%s, ecount: %d RET: %s', username, ecount, RET)
                SALTRET = ret_process(RET, dtype='init')
                # logger.info('%s, SALTRET: %s', username, SALTRET)

                # for elment in RET:
                #  SALTRET[elment] = json.dumps(RET[elment],indent=1)
