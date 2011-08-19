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
        cur = self._database.get_cursor()
        cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = '%s'" % (self.name))
        tables = []
        for table in cur:
            tables.append(table[0])
        cur.close()
        
        return tables
    
    
    
    