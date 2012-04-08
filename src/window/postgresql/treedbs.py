# -*- coding: utf-8 -*-


from window.windowgeneric import treedbs
from window import stock, events



class TreeDbs(treedbs.TreeDbs):
    
    def _do_on_select(self, widget):
        cursor = widget.get_cursor()[0]
        iter = self._store.get_iter(cursor)
        value = self._store.get_value(iter, 1)
        
        expand = self.__select_table(cursor, iter, value)
    
        if expand:
            self._treeView.expand_row(self._store.get_path(iter), False)

    
    def __select_table(self, cursor, iter, value):
        expand = False
        try:
            cursor[3]
        except IndexError:
            expand = self.__select_schema(cursor, iter, value)
        else:
            events.send(events.SELECTED_TABLE, True, self._store.get_table(value))

        return expand
    
    def __select_schema(self, cursor, iter, value):
        expand = False
        try:
            cursor[2]
        except IndexError:
            expand = self.__select_database(cursor, iter, value)
        else:
            self._store.set_schema_selected(value)
            if self._store.iter_children(iter) == None:
                self._store.load_tables(iter)
                expand = True
            
            events.send(events.SELECTED_SCHEMA, True, self._store.get_schema_selected())
            
        return expand
        
    def __select_database(self, cursor, iter, value):
        expand = False
        try:
            cursor[1]
        except IndexError:
            expand = self.__select_host(cursor, iter, value)
        else:
            self._store.set_database_selected(value)
            if self._store.iter_children(iter) == None:
                self._store.load_schemas(iter)
                expand = True
            events.send(events.SELECTED_DATABASE, True)
            
        return expand
    
    def __select_host(self, cursor, iter, value):
        events.send(events.SELECTED_SERVER)
        return False


class StoreDbs(treedbs.StoreDbs):
    
    def set_schema_selected(self, name):
        self.__schemaSelected = self.get_database_selected().get_schema(name)
        
    def get_schema_selected(self):
        return self.__schemaSelected
    
    def get_table(self, name):
        return self.get_schema_selected().get_table(name)
    
    def load_schemas(self, iter):
        schemas = self.get_database_selected().get_schemas()
        for schema in schemas:
            self.append(iter, [stock.STOCK_NAMESPACE, schema])
    
    def load_tables(self, iter):
        tables = self.get_schema_selected().get_tables()
        for table in tables:
            self.append(iter, [stock.STOCK_TABLE, table.name])
