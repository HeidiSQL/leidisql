# -*- coding: utf-8 -*-

import gtk
from window import events, stock, general
import window

class Manager(object):
    
    
    def __init__(self, host):
        self._host = host
                
        self._main_container = gtk.Notebook()
        
        widgetHost = self.__host()
        widgetHost.show_all()
        self._main_container.append_page(widgetHost, gtk.Label(_("Host: %s")))
        
        # tabs hidden
        self._main_container.append_page(self.__tab_schema(), gtk.Label(_("Schema: %s")))
        self._main_container.append_page(self.__tab_table(), gtk.Label(_("Table: %s")))
        self._main_container.append_page(self.__tab_table_data(), gtk.Label(_("Data")))
        
        
        
        query = self.__tab_query()
        query.show_all()
        self._main_container.append_page(query, gtk.Label(_("Query")))
        self._main_container.show()
        
        # connect
        events.connect(events.SELECTED_SERVER, self.server_selected)
        events.connect(events.SELECTED_SCHEMA, self.schema_selected)
        events.connect(events.SELECTED_TABLE, self.table_selected)
        
    
    def __host(self):
        tabs = gtk.Notebook()
        
        tabs.append_page(self.__tab_databases(), gtk.Label(_("Databases (%d)")))
        tabs.append_page(self.__tab_variables(), gtk.Label(_("Variables (%d)")))
        tabs.append_page(self.__tab_status(), gtk.Label(_("Status (%s)")))
        tabs.append_page(self.__tab_processes(), gtk.Label(_("Processes (%s)")))
        tabs.append_page(self.__tab_command_statics(), gtk.Label(_("Command-Statistics (%d)")))
        
        return tabs
        
    def __tab_databases(self):
        hbox = gtk.HBox()
        return hbox
    
    def __tab_variables(self):
        hbox = gtk.HBox()
        return hbox
    
    def __tab_status(self):
        hbox = gtk.HBox()
        return hbox
    
    def __tab_processes(self):
        hbox = gtk.HBox()
        return hbox
    
    def __tab_command_statics(self):
        hbox = gtk.HBox()
        return hbox


    def __tab_schema(self):
        self._tabSchema = TabSchema()
        return self._tabSchema
    
    def __tab_table(self):
        self._tabTable = TabTable() 
        return self._tabTable
    
    def __tab_table_data(self):
        self._tabTableData = TableData()
        return self._tabTableData
    
    def __tab_query(self):
        hbox = gtk.HBox()
        return hbox
    
    
    def server_selected(self):
        self.schema_selected(False)
        self._main_container.set_current_page(0)
    
    def schema_selected(self, show, schema=None):
        if show:
            self._main_container.get_nth_page(1).show()
            self._main_container.set_current_page(1)
            self.table_selected(False)
        else:
            self._main_container.get_nth_page(1).hide()
            self._main_container.get_nth_page(2).hide()
            
        if schema != None:
            self._tabSchema.set_schema(schema)
    
    def table_selected(self, show, table=None):
        if show:
            self._main_container.get_nth_page(2).show()
            self._main_container.get_nth_page(3).show()
            self._main_container.set_current_page(2)
        else:
            self._main_container.get_nth_page(2).hide()
            self._main_container.get_nth_page(3).hide()
            
        if table != None:
            self._tabTable.set_table(table)
            self._tabTableData.set_table(table)
    
    def main_container(self):
        return self._main_container
    

class TabSchema(window.general.ScrolledWindow):
    
    COLUMN_NAME = 1
    COLUMN_OWNER = 2
    COLUMN_TYPE = 3
    
    def __init__(self):
        super(TabSchema, self).__init__()
        
        self._sortColumnId = TabSchema.COLUMN_NAME
        self._sortColumnOrder = gtk.SORT_ASCENDING
        
        self._store = gtk.ListStore(str, str, str, str)
        
        self._treeView = gtk.TreeView(self._store)
        
        self.__column_name()
        self.__column(_("Owner"), TabSchema.COLUMN_OWNER)
        self.__column(_("Type"), TabSchema.COLUMN_TYPE)
        
        self.add(self._treeView)
        self.show_all()
    
    def __column_name(self):
        column = gtk.TreeViewColumn(_("Name"))
        self._treeView.append_column(column)
        
        cell_pixbuf = gtk.CellRendererPixbuf()
        column.pack_start(cell_pixbuf, False)
        column.set_attributes(cell_pixbuf, stock_id=0)
        
        cell_text = gtk.CellRendererText()
        column.pack_start(cell_text)
        column.add_attribute(cell_text, "text", TabSchema.COLUMN_NAME)
        
    def __column(self, name, id):
        column = gtk.TreeViewColumn(name)
        self._treeView.append_column(column)
        
        cell_text = gtk.CellRendererText()
        column.pack_start(cell_text)
        column.add_attribute(cell_text, "text", id)
        
    def set_schema(self, schema):
        tables = schema.get_tables()
        self._store.clear()
        for table in tables:
            self._store.append([stock.STOCK_TABLE, table.name, table.name, table.type])
            
        self._store.set_sort_column_id(self._sortColumnId, self._sortColumnOrder)
            


class TabTable(gtk.VBox):
    
    def __init__(self):
        super(TabTable, self).__init__()
        
        vpaned = gtk.VPaned()
        vpaned.set_position(200)
        vpaned.add1(self.__conf_table())
        vpaned.add2(self.__columns())
        self.pack_start(vpaned)

        self.pack_start(self.__bts(), False, False, 0)
        
        self.show_all()
    
    def __conf_table(self):
        tabs = gtk.Notebook()
        tabs.append_page(self.__tab_basic(), gtk.Label(_("Basic")))
        tabs.append_page(self.__tab_options(), gtk.Label(_("Options")))
        tabs.append_page(self.__tab_indexes(), gtk.Label(_("Indexes")))
        tabs.append_page(self.__tab_foreign_keys(), gtk.Label(_("Foreign Keys")))
        tabs.append_page(self.__tab_create_code(), gtk.Label(_("CREATE code")))
        tabs.append_page(self.__tab_alter_code(), gtk.Label(_("ALTER code")))
        return tabs
    
    def __tab_basic(self):
        vbox = gtk.VBox()
        
        nameHbox = gtk.HBox()
        vbox.pack_start(nameHbox, False, False, 0)
        
        nameLabel = gtk.Label(_("Name")  + ":")
        nameLabel.set_width_chars(10)
        nameLabel.set_alignment(0, 0)
        nameHbox.pack_start(nameLabel, False, False, 0)
        
        nameEntry = gtk.Entry()
        nameHbox.pack_start(nameEntry)
        
        commentHbox = gtk.HBox()
        vbox.pack_start(commentHbox)
        
        commentLabel = gtk.Label(_("Comment") + ":")
        commentLabel.set_width_chars(10)
        commentLabel.set_alignment(0, 0)
        commentHbox.pack_start(commentLabel, False, False, 0)
        
        commentText = gtk.TextView()
        commentText.set_editable(True)
        commentText.set_size_request(-1, 250)
        commentScrooled = general.ScrolledWindow()
        commentScrooled.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
        commentScrooled.add(commentText)
        commentHbox.pack_start(commentScrooled)
        
        return vbox
    
    def __tab_options(self):
        hbox = gtk.HBox()
        return hbox
    
    def __tab_indexes(self):
        hbox = gtk.HBox()
        return hbox
    
    def __tab_foreign_keys(self):
        hbox = gtk.HBox()
        return hbox
    
    def __tab_create_code(self):
        hbox = gtk.HBox()
        return hbox
    
    def __tab_alter_code(self):
        hbox = gtk.HBox()
        return hbox
    
    def __columns(self):
        self._listStoreColumns = gtk.ListStore(str, str)
        self._listColumns = gtk.TreeView(self._listStoreColumns)
        return self._listColumns

    def __bts(self):
        fixed = gtk.Fixed()
        
        btHelp = gtk.Button()
        btHelp.set_label(_("Help")) 
        btHelp.set_size_request(100, -1)
        fixed.put(btHelp, 0, 0)
        
        btDiscard = gtk.Button()
        btDiscard.set_label(_("Discard")) 
        btDiscard.set_size_request(100, -1)
        fixed.put(btDiscard, 100, 0)
        
        btSave = gtk.Button()
        btSave.set_label(_("Save")) 
        btSave.set_size_request(100, -1)
        fixed.put(btSave, 200, 0)
        
        return fixed
        
    def set_table(self, table):
        self._table = table
        print table
        
        
    def __populate_columns(self):
        pass
    
    
class TableData(gtk.VBox):
    
    def __init__(self):
        super(TableData, self).__init__()
        
        self._treeView = gtk.TreeView()
        
    
    def set_table(self, table):
        self._table = table
    
    def __load_columns(self):
        columns = []
        for column in self._table.get_columns():
            columns.append(column)
            
        return column
        
    def __column(self, name):
        column = gtk.TreeViewColumn(name)
        self._treeView.append_column(column)
        
        cell_text = gtk.CellRendererText()
        column.pack_start(cell_text)
        column.add_attribute(cell_text, "text", TabSchema.COLUMN_NAME)
        
        