# -*- coding: utf-8 -*-

import xmlrpclib

class supervisortools:
    """supervisor辅助工具"""

    def __init__(self, host, port=9001, username='root', password='viiv'):
        uri = 'http://%s:%s@%s:%s/RPC2' % (username, password, host, port)
        self.host = host
        self.server = xmlrpclib.Server(uri)
        self.op_result = {'host': host, 'status':0, 'msg': u'操作成功'}

    def getProcessInfo(self, name):
        info = self.server.supervisor.getProcessInfo(name)
        info['host'] = self.host
        return info

    def startProcess(self, name):
        bret = self.server.supervisor.startProcess(name)
        if not bret:
            self.op_result['status'] = 1
            self.op_result['msg'] = u'操作失败'
        return self.op_result

    def stopProcess(self, name):
        bret = self.server.supervisor.stopProcess(name)
        if not bret:
            self.op_result['status'] = 1
            self.op_result['msg'] = u'操作失败'
        return self.op_result

    def restartProcess(self, name):
        result = self.stopProcess(name)
        if result['status'] != 0:
            info = self.getProcessInfo(name)
            if info['state'] == 20:
                # 关闭进程失败
                return result

        result = self.startProcess(name)
        return result

def test():
    sp = supervisortools('10.1.0.40')
    print(sp.getProcessInfo())

if __name__ == '__main__':
    test()
