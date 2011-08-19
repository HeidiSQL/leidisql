# -*- coding: utf-8 -*-

import gtk
from window import events

class Manager():
    
    
    def __init__(self):
        self._main_container = gtk.Notebook()
        
        widgetHost = self.__host()
        widgetHost.show_all()
        self._main_container.append_page(widgetHost, gtk.Label(_("Host: %s")))
        
        # tabs hidden
        self._main_container.append_page(self.__database_selected(), gtk.Label(_("Database: %s")))
        self._main_container.append_page(self.__table_selected(), gtk.Label(_("Table: %s")))
        self._main_container.append_page(self.__data_table_selected(), gtk.Label(_("Data")))
        
        
        
        query = self.__query()
        query.show_all()
        self._main_container.append_page(query, gtk.Label(_("Query")))
        self._main_container.show()
        
        # connect
        events.connect(events.SELECTED_DATABASE, self.host_selected)
        
    
    def __host(self):
        tabs = gtk.Notebook()
        
        tabs.append_page(self.__databases(), gtk.Label(_("Databases (%d)")))
        tabs.append_page(self.__variables(), gtk.Label(_("Variables (%d)")))
        tabs.append_page(self.__status(), gtk.Label(_("Status (%s)")))
        tabs.append_page(self.__processes(), gtk.Label(_("Processes (%s)")))
        tabs.append_page(self.__command_statics(), gtk.Label(_("Command-Statistics (%d)")))
        
        return tabs
    
    def __database_selected(self):
        hbox = gtk.HBox()
        return hbox
    
    def __databases(self):
        hbox = gtk.HBox()
        return hbox
    
    def __table_selected(self):
        hbox = gtk.HBox()
        return hbox
    
    def __data_table_selected(self):
        hbox = gtk.HBox()
        return hbox
    
    def __variables(self):
        hbox = gtk.HBox()
        return hbox
    
    def __status(self):
        hbox = gtk.HBox()
        return hbox
    
    def __processes(self):
        hbox = gtk.HBox()
        return hbox
    
    def __command_statics(self):
        hbox = gtk.HBox()
        return hbox
    
    def __query(self):
        hbox = gtk.HBox()
        return hbox
    
    
    def host_selected(self, show):
        print "Passsou"
        if show:
            self._main_container.get_nth_page(1).show()
        else:
            self._main_container.get_nth_page().hide()
    
    def main_container(self):
        return self._main_container