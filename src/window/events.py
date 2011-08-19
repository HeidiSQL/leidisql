# -*- coding: utf-8 -*-


from blinker import signal

SELECTED_SERVER = "selected-server"
SELECTED_DATABASE = "selected-database"
SELECTED_SCHEMA = "selected-schema"


def send(event, sender=1):
    print "send", event
    signal(event).send(sender)
    
def connect(event, callback):
    print "connect", event, callback
    signal(event).connect(callback)