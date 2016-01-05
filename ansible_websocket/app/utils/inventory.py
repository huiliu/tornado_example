#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# file: utile/inventory.py
# description: 解析ansible的inventory文件，返回其中的主机组信息
# DateTime: 2015-12-04 01:57
#

from ansible import inventory
import ansible.playbook
from ansible import callbacks
from ansible import utils
from ansible.callbacks import display
from ansible.color import ANSIBLE_COLOR
import os
from collections import OrderedDict


#_inventory_file = 'operation_scripts/inventory'
inventory_source = 'operation_scripts/inv.py'


def get_inventory_info(inv_file=inventory_source):
    """
    """
    print(os.getcwd())
    if not os.path.isfile(inv_file):
        return
    inv = inventory.Inventory(inv_file)

    ret_dict = OrderedDict()
    for grp in inv.get_groups():
        host_list = list()
        for host in grp.get_hosts():
            host_list.append(host.name)

        ret_dict[grp.name] = host_list

    return ret_dict

class OpPlaybook:
    """对ansible.playbook进行简单包装
    """

    def __init__(self, inventory, playbook, only_tags=None, skip_tags=None,
            subset=None, desc=None):
        self.hosts       = sorted(set())
        self.tasks       = sorted(set())
        self.tags        = []
        self.inventory   = inventory
        self.playbook    = playbook
        self.only_tags   = only_tags
        self.skip_tags   = skip_tags
        self.description = desc
        self.pb          = None
        self.subset      = subset

    def _get_pb(self):
        if not self.pb:
            inventory = ansible.inventory.Inventory(self.inventory)
            inventory.subset(self.subset)

            stats = callbacks.AggregateStats()
            self.playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
            # 任务执行日志会通过sys.stdout输出
            runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)
            
            self.pb = ansible.playbook.PlayBook(
            		playbook=self.playbook,
            		inventory=inventory,
                    only_tags=self.only_tags,
                    skip_tags=self.skip_tags,
            		stats=stats,
            		callbacks=self.playbook_cb,
            		runner_callbacks=runner_cb
            		#check=True
            		)
        return self.pb


    def _collect_data(self):
        pb = self._get_pb()

        for (play_ds, play_basedir) in zip(pb.playbook, pb.play_basedirs):
            play = ansible.playbook.Play(pb, play_ds, play_basedir,
                                          vault_password=pb.vault_password)
            label = play.name
            self.hosts = pb.inventory.list_hosts(play.hosts)
        
            for task in pb.tasks_to_run_in_play(play):
            	self.tags.extend(task.tags)
        
            for task in pb.tasks_to_run_in_play(play):
                if getattr(task, 'name', None) is not None:
               	    self.tasks.append((task.name, ', '.join(sorted(set(task.tags).difference(['untagged'])))))

    def get_hosts(self):
        if not self.hosts:
            self._collect_data()

        return self.hosts

    def get_tasks(self):
        if not self.tasks:
            self._collect_data()
        return self.tasks

    def get_tags(self):
        assert False
        return self.tags

    def run_task(self):
        pb = self._get_pb()

        # TODO: 捕捉每个任务的执行结果
        # 需要重写一个callbacks类
        return pb.run();

    def get_description(self):
        return self.description


def PlayBookFactory(t, only_tags=None, skip_tags=None,
        inventory=inventory_source, subset=None, private_key_file=None):
    """
    """
    playbook_files = {
            "compile": "op/compile.yml",
            "production": "../../op/production.yml",
            "database": "op/database.yml",
            "webserver": "op/webserver.yml",
            "release": "op/release.yml"
            }
    playbook_description = {
            "compile": u"编译服",
            "production": u"我欲封服务器",
            "database": u"数据库服务器",
            "webserver": u"Web服务器",
            "release": u"发布"
            }

    if subset.lower() == 'all':
        subset = None

    ret = None
    t = t.lower()
    if t in playbook_files:
        ret = OpPlaybook(inventory,
                        playbook_files[t],
                        only_tags,
                        skip_tags,
                        subset,
                        playbook_description[t])

    return ret

def test():
    p = PlayBookFactory('production', ['all'], subset='all',
            inventory='../../op/inventory')
    p.run_task()

if __name__ == '__main__':
    test()
