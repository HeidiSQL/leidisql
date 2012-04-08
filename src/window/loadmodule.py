# -*- coding: utf-8 -*-

import hosts

def instance_TreeDbs(host):
    if host.type.get_type() == hosts.Type.POSTGRELSQL_TCP_IP:
        from window.postgresql.treedbs import TreeDbs as Tree
        from window.postgresql.treedbs import StoreDbs as Store
    
    
    tree =  Tree(host, Store(host))
    return tree

def instance_manager(host):
    if host.type.get_type() == hosts.Type.POSTGRELSQL_TCP_IP:
        from window.postgresql.manager import Manager as Manager
    
    
    return Manager(host)