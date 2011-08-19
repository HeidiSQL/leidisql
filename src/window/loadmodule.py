# -*- coding: utf-8 -*-

import hosts
import window, gtk

def instance_TreeDbs(host):
    if host.type.get_type() == hosts.Type.POSTGRELSQL_TCP_IP:
        from window.postgresql.treedbs import TreeDbs as Tree
        from window.postgresql.treedbs import StoreDbs as Store
    
    
    tree =  Tree(host, Store(host))
    return tree
    scrolledWindow = gtk.ScrolledWindow()
    scrolledWindow.add(tree)
    
    return scrolledWindow

def instance_manager(host):
    if host.type.get_type() == hosts.Type.POSTGRELSQL_TCP_IP:
        from window.postgresql.manager import Manager as Manager
    
    
    return Manager()