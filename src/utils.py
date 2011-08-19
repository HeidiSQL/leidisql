# -*- coding: utf-8 -*-

import os
from posixpath import dirname

__icons_dir = None
__res_dir = None
__root_dir = None


def get_res_icons(name):
    global __icons_dir
    if __icons_dir is None:
       __icons_dir = os.sep.join([get_res_dir(), "icons"])
    
    return os.sep.join([__icons_dir, name])

def get_res_dir():
    global __res_dir
    if __res_dir is None:
       __res_dir = os.sep.join([get_root_path(), 'res'])
    
    return __res_dir

def get_root_path():
    global __root_dir
    
    if os.name != 'nt':
        if __root_dir is None:
            __root_dir = dirname(__file__)
    else:
        if __root_dir is None:
            __root_dir = os.path.join(".", "res")
            
    return __root_dir

def get_save_dir ():
    try:
        base = os.environ['HOME']
    except:
        base = os.environ['USERPROFILE']
        
    if os.name != 'nt':
        dirname = os.path.join(base, ".heidsql" + os.sep)
    else:
        dirname = os.path.join(base, ".heidsql" + os.sep)
        
    if not os.access(dirname, os.W_OK):
        os.makedirs(dirname)
        
    return dirname