# -*- coding: utf-8 -*-


from window.windowgeneric import treedbs
from window import stock, events
from blinker import signal



class TreeDbs(treedbs.TreeDbs):
    
    def _do_on_select_db(self, widget):
        cursor = widget.get_cursor()[0]
        iter = self._store.get_iter(cursor)
        expand = False
        
        try:
            # selected schema
            cursor[2]
        except IndexError:
            try:
                # selected database
                cursor[1]
            except IndexError:
                # selected host
                events.send(events.SELECTED_SERVER)
            else:
                self._store.set_database_selected(self._store.get_value(iter, 1))
                if self._store.iter_children(iter) == None:
                    self._store.load_schemas(iter)
                    expand = True
                
                events.send(events.SELECTED_DATABASE, True)
        else:
            self._store.set_schema_selected(self._store.get_value(iter, 1))
            if self._store.iter_children(iter) == None:
                self._store.load_tables(iter)
                expand = True
                
            events.send(events.SELECTED_SCHEMA)
            
        if expand:
            self._treeView.expand_row(self._store.get_path(iter), False)



class StoreDbs(treedbs.StoreDbs):
    
    def set_schema_selected(self, name):
        self.__schemaSelected = self.get_database_selected().get_schema(name)
        
    def get_schema_selected(self):
        return self.__schemaSelected
    
    def load_schemas(self, iter):
        schemas = self.get_database_selected().get_schemas()
        for schema in schemas:
            self.append(iter, [stock.STOCK_NAMESPACE, schema])
    
    def load_tables(self, iter):
        tables = self.get_schema_selected().get_tables()
        for table in tables:
            self.append(iter, [stock.STOCK_TABLE, table])
