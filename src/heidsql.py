#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import gtk
from window import general

from i18n import _

class HeidSQL(object):
    def __init__ (self):
        general.SessionManager()
        
if __name__ == "__main__":
    HeidSQL()
    gtk.main()