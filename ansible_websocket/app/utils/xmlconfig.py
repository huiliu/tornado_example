# -*- coding: utf-8 -*-
from xml.etree import ElementTree


class SvrConfigXml:
    """检查各字段的有效性，并生成XML配置文件
    """

    # 此处字段名**必须**与ServerConfigForm一致
    cluster_name     = ""
    region_id        = ""

    maps             = ""
    dungeons_map     = ""

    char_db_host     = ""
    char_db_name     = ""
    char_db_username = ""
    char_db_password = ""

    log_db_host      = ""
    log_db_name      = ""
    log_db_username  = ""
    log_db_password  = ""

    tpl_index_file   = ""
    script_dir       = ""

    auth_pwd_url     = ""
    auth_token_url    = ""

    dyn_config_url   = ""

    server_host_ip   = ""

    loginsvr_port    = ""
    gatesvr_port     = ""
    chatsvr_port     = ""


    def data(self):
        cluster_tree = ElementTree.Element('cluster_configuration')
        cluster_tree.set('name', self.cluster_name)
        cluster_tree.set('region_uid', str(self.region_id))
        
        map_ele = ElementTree.SubElement(cluster_tree, 'maps')
        map_ele.set('sequence', self.maps)
        map_ele.set('dungeons', self.dungeons_map)
        
        char_db_ele = ElementTree.SubElement(cluster_tree, 'dbsvr')
        char_db_ele.set('hostname', self.char_db_host)
        char_db_ele.set('database', self.char_db_name)
        char_db_ele.set('username', self.char_db_username)
        char_db_ele.set('password', self.char_db_password)
        
        log_db_ele = ElementTree.SubElement(cluster_tree, 'logdbsvr')
        log_db_ele.set('hostname', self.log_db_host)
        log_db_ele.set('database', self.log_db_name)
        log_db_ele.set('username', self.log_db_username)
        log_db_ele.set('password', self.log_db_password)
        
        data_path_ele = ElementTree.SubElement(cluster_tree, 'path')
        data_path_ele.set('svrpath', self.tpl_index_file)
        data_path_ele.set('scriptfolder', self.script_dir)
        
        auth_svr0 = ElementTree.SubElement(cluster_tree, 'authsvr0')
        auth_svr0.set('type', 'password')
        auth_svr0.set('url', self.auth_pwd_url)
        auth_svr0.set('key', '')
        auth_svr0.set('extra', '')
        
        auth_svr1 = ElementTree.SubElement(cluster_tree, 'authsvr1')
        auth_svr1.set('type', 'token')
        auth_svr1.set('url', self.auth_token_url)
        auth_svr1.set('key', '')
        
        dyncfg_ele = ElementTree.SubElement(cluster_tree, 'dynconfig')
        dyncfg_ele.set('url', self.dyn_config_url)
        
        host_ele = ElementTree.SubElement(cluster_tree, 'host')
        host_ele.set('wanip', self.server_host_ip)
        
        gamesvr_ele = ElementTree.SubElement(host_ele, 'service')
        gamesvr_ele.set('type', 'gamesvr')
        gamesvr_ele.set('port', '49121')
        gamesvr_ele.set('line', '1')
        gamesvr_ele.set('map', '1,2,3')
        
        npcsvr_ele = ElementTree.SubElement(host_ele, 'service')
        npcsvr_ele.set('type', 'npcsvr')
        npcsvr_ele.set('line', '1')
        npcsvr_ele.set('map', '1,2,3')
        
        tracksvr_ele = ElementTree.SubElement(host_ele, 'service')
        tracksvr_ele.set('type', 'tracksvr')
        tracksvr_ele.set('port', '49120')
        
        chatsvr_ele = ElementTree.SubElement(host_ele, 'service')
        chatsvr_ele.set('type', 'chatsvr')
        chatsvr_ele.set('port', str(self.chatsvr_port))
        
        loginsvr_ele = ElementTree.SubElement(host_ele, 'service')
        loginsvr_ele.set('type', 'loginsvr')
        loginsvr_ele.set('port', str(self.loginsvr_port))
        
        gatesvr_ele = ElementTree.SubElement(host_ele, 'service')
        gatesvr_ele.set('type', 'gatesvr')
        gatesvr_ele.set('port', str(self.gatesvr_port))
        
        gatesvr_ele = ElementTree.SubElement(host_ele, 'service')
        gatesvr_ele.set('type', 'logsvr')
        gatesvr_ele.set('port', '49116')
        
        return ElementTree.tostring(cluster_tree)


class DynConfigXml:
    """
    """
    combat_exp_rate                    = ""
    instance_max_count                 = ""
    currency_rmb_gold_rate             = ""
    game_max_speed_scale               = ""
    login_maxusercount                 = ""
    mission_award_exprate                 = ""
    game_enable_dragback               = ""
    disconnect_cooldown                = ""
    stone_compose_quality_limit        = ""
    operate_flags                      = ""
    role_max_level                     = ""
    map_max                            = ""
    return_equipupperexp_rate          = ""
    trumpequipupper_consume_money_rate = ""
    sys_gamestore                      = ""

    def data(self):

        self.param_tree = ElementTree.Element('svr_params')

        self._add_param('combat.exp.rate',                    self.combat_exp_rate)
        self._add_param('instance.max.count',                 self.instance_max_count)
        self._add_param('currency.rmb.gold.rate',             self.currency_rmb_gold_rate)
        self._add_param('game.max.speed.scale',               self.game_max_speed_scale)
        self._add_param('login.maxusercount',                 self.login_maxusercount)
        self._add_param('mission.award.exprate',              self.mission_award_exprate)
        self._add_param('game.enable.dragback',               self.game_enable_dragback)
        self._add_param('disconnect.cooldown',                self.disconnect_cooldown)
        self._add_param('stone.compose.quality.limit',        self.stone_compose_quality_limit)
        self._add_param('operate.flags',                      self.operate_flags)
        self._add_param('role.max.level',                     self.role_max_level)
        self._add_param('map.max',                            self.map_max)
        self._add_param('return.equipupperexp.rate',          self.return_equipupperexp_rate)
        self._add_param('trumpequipupper.consume.money.rate', self.trumpequipupper_consume_money_rate)

        gamestore = "enable"
        if not self.sys_gamestore:
            gamestore = 'disable'

        self._add_param('sys_gamestore',                      gamestore)

        return ElementTree.tostring(self.param_tree)

    def _add_param(self, name, value):
        map_ele = ElementTree.SubElement(self.param_tree, 'param')
        map_ele.set('name', name)
        map_ele.set('value', str(value))
