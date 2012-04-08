# -*- coding: utf-8 -*-



SELECTED_SERVER = "selected-server"
SELECTED_DATABASE = "selected-database"
SELECTED_SCHEMA = "selected-schema"
SELECTED_TABLE = "selected-table"


__events = {}

def send(event, *kargs):
    try:
        __events[event]
    except KeyError:
        pass
    else:
        return __events[event](*kargs)
    
    
def connect(event, callback):
    __events[event] = callback