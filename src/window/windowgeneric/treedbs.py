# -*- coding: utf-8 -*-

import gtk
from window import stock
import window


class TreeDbs(window.general.ScrolledWindow):
    
    def __init__(self, host, store):
        super(TreeDbs, self).__init__()
        
        self._host = host
        self._store = store
        
        self._treeView = gtk.TreeView(store)
        self.add(self._treeView)
        
        column = gtk.TreeViewColumn("")
        self._treeView.append_column(column)
        
        cell_pixbuf = gtk.CellRendererPixbuf()
        column.pack_start(cell_pixbuf, False)
        column.set_attributes(cell_pixbuf, stock_id=0)
        
        cell_text = gtk.CellRendererText()
        column.pack_start(cell_text, True)
        column.add_attribute(cell_text, "text", 1)
        
        
        self._treeView.expand_row(0, False)
        
        self._treeView.connect("cursor-changed", self._do_on_select_db)
        
        #self.pack_start(self.__scrool_bar(), False, False, 0)
        
        self.show_all()
    
    def __scrool_bar(self):
        return gtk.VScrollbar(self._treeView.get_vadjustment())
    
    def _do_store(self):
        raise NotImplementedError()
    
    def _do_on_select_db(self, widget):
        raise NotImplementedError()
        


class StoreDbs(gtk.TreeStore):
    
    def __init__(self, host):
        super(gtk.TreeStore, self).__init__()
        self.set_column_types(str, str)
        self._host = host
        
        self.set_sort_column_id(1, gtk.SORT_ASCENDING)
        
        root = self.append(None, [stock.STOCK_SERVER, self._host.name])
        for name in host.get_databases_name():
            parent = self.append(root, [stock.STOCK_DATABASE, name])
        
    def get_database_selected(self):
        return self.__databaseSelected
    
    def set_database_selected(self, name):
        self.__databaseSelected = self._host.get_database(name)
        