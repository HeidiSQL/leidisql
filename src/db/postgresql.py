# -*- coding: utf-8 -*-

import psycopg2 as dbapi2
from db import relational


class Databases(relational.ABCDatabases):
    
    def __init__(self, host):
        self._host = host
        self._databases = {}
        self._DSN = "dbname=%s host=%s user=%s password=%s" % ("%s", host.address, host.user, host.password)
        DSN = self._DSN % ("postgres")
        self._co = dbapi2.connect(DSN)
        dbapi2.extensions.register_type(dbapi2.extensions.UNICODE)
        dbapi2.extensions.register_type(dbapi2.extensions.UNICODEARRAY)
    
    def __del__(self):
        self._co.close()
        
    def get_databases_name(self):
        cur = self.__get_cursor()
        cur.execute("SELECT datname FROM pg_database")
        names = set()
        for record in cur:
            names.add(record[0])
        cur.close()
        return names
    
    def get_database(self, name):
        try:
            database = self._databases[name]
        except KeyError:
            database = self._databases[name] = Database(self._host, name, self._DSN % (name))
        
        return database
    
    def __get_cursor(self):
        return self._co.cursor()
        

class Database(object):
    
    def __init__(self, host, name, DSN):
        self.name = name
        self._host = host
        self._schemas = {}
        self._co = dbapi2.connect(DSN)
        dbapi2.extensions.register_type(dbapi2.extensions.UNICODE)
        dbapi2.extensions.register_type(dbapi2.extensions.UNICODEARRAY)
    
    def get_schemas(self):
        schemas = []
        cur = self.get_cursor()
        cur.execute("SELECT schema_name FROM information_schema.schemata")
        for schema in cur:
            schemas.append(schema[0])
        cur.close()
            
        return schemas
    
    def get_schema(self, name):
        try:
            schema = self._schemas[name]
        except KeyError:
            schema = self._schemas[name] = Schema(self, name)
        
        return schema
    
    def get_cursor(self):
        return self._co.cursor()
    
    
    #select column_name from INFORMATION_SCHEMA.COLUMNS where table_name = 'table'; 
        
        
class Schema(object):
    
    def __init__(self, database, name):
        self.name = name
        self._database = database
    
    def get_tables(self):
        return self.__find_tables("table_schema = '%s'" % (self.name))
    
    def get_table(self, name):
        return self.__find_tables("table_schema = '%s' AND table_name = '%s'" % (self.name, name))[0]
        
    def __find_tables(self, where):
        cur = self._database.get_cursor()
        cur.execute("SELECT table_name, table_type " +
                    "FROM information_schema.tables " + 
                    "WHERE " + where)
        tables = []
        for table in cur:
            tables.append(Table(self._database, table[0], table[1]))
        cur.close()
        return tables

class Table(object):
    
    def __init__(self, database, name, type):
        self._database = database
        self.name = name
        self.type = type
        
        
    def get_columns(self):
        return self.__find_columns("table_catalog = '%s' " +
                                   "AND table_schema = '%s'", 
                                   (self._database.name, self.name))

    def get_column(self, name):
        return self.__find_columns("table_catalog = '%s' " + 
                                   "AND table_schema = '%s' " + 
                                   "AND table_name",
                                   (self._database.name, self.name, name))
        
    def __find_columns(self, where):
        cur = self._database.get_cursor()
        cur.execute("SELECT column_name " +
                    "FROM information_schema.columns " + 
                    "WHERE " + where)
        
        columns = []
        for column in cur:
            columns.append(Column(self._database, column[0]))
        cur.close()
        return columns

    def get_indexes(self):
        pass


class Column(object):
    
    def __init__(self, database, name):
        self._database = database
        self.name = name

    