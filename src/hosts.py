# -*- coding: utf-8 -*-

import importlib
import anydbm
import pickle
import utils
import i18n

class List(object):
    
    DB = utils.get_save_dir() + 'hosts.db'
    
    def __init__(self):
        self._hosts = anydbm.open(List.DB, 'c')
        
    def __del__(self):
        self._hosts.close()
    
    def get(self, index):
        return pickle.loads(self._hosts[index])
    
    def add(self, host):
        assert isinstance(host, Host)
        
        if host.name == None:
            raise ExceptHostNameInvalid("host.name is None") 
        
        if host.name in self._hosts:
            raise ExceptHostNameExist("host.name exist")
        
        self.save(host)
    
    def save(self, host):
        assert isinstance(host, Host)
        self._hosts[host.name] = pickle.dumps(host)
    
    def remove(self, host):
        if host != None:
            del self._hosts[host.name]

    def iteritems(self):
        items = []
        type(self._hosts.keys())
        for k in self._hosts.keys():
            items.append(self.get(k))
        
        return items
    
    def create_host(self):
        i = ""
        name = _("Unnamed").encode()
        while name + ((i != "" or "") and "-" + str(i)) in self._hosts:
            if i == "":
                i = 1
            else:
                i += 1
        
        if i != "":
            name += "-" + str(i)
        
        return Host(name, Type.create_type(Type.MYSQL_TCP_IP))
        
    
class ExceptHostNameExist(Exception):
    pass


class Host(object):
    
    def __init__(self, name, type):
        if name == None:
            raise ExceptHostNameInvalid("Name invalid")
        
        self.type = type
        self.name = name
        self.port = self.type.get_port_default()
        self.address = "localhost" 
        self.user = self.password = ""
    
    def get_databases_name(self):
        return self.get_databases().get_databases_name()
    
    def get_database(self, name):
        return self.get_databases().get_database(name)
    
    def get_databases(self):
        try:
            self._databases
            
        except AttributeError:
            type = self.type.get_type()
            if type == Type.POSTGRELSQL_TCP_IP:
                from db.postgresql import Databases
                
            elif type == Type.MYSQL_TCP_IP:
                from db.mysql import Databases
            
            self._databases = Databases(self)
        
        return self._databases
    
class ExceptHostNameInvalid(Exception):
    pass


class Type(object):
    
    MYSQL_TCP_IP = 0
    MYSQL_NAMED_PIPE = 1
    MYSQL_SSH_TUNEL = 2
    
    POSTGRELSQL_TCP_IP = 3
    
    
    TAB_SETTINGS  = 0
    TAB_SSL_OPTIONS = 1
    TAB_SSH_TUNEL = 2
    TAB_STATISTCS = 3
    
    
    FIELD_TYPE = 0
    FIELD_ADDRESS = 1
    FIELD_USER = 2
    FIELD_PASSWORD = 3
    FIELD_PROMPT = 4
    FIELD_PORT = 5
    FIELD_COMPRESSED = 6
    FIELD_DATABASES = 7
    FIELD_STARTUP_SCRIPT = 8
    
    __all_bds = {MYSQL_TCP_IP: "MySQL (TCP/IP)",
                 MYSQL_NAMED_PIPE: "MySQL (named pipe)",
                 MYSQL_SSH_TUNEL: "MySQL (SSH tunnel)",
                 POSTGRELSQL_TCP_IP: "PostrgreSQL (TCP/IP)"
                 }
    
    __port_default = {MYSQL_TCP_IP: "3306",
                      MYSQL_NAMED_PIPE: "",
                      MYSQL_SSH_TUNEL: "3306",
                      POSTGRELSQL_TCP_IP: ""
                      }
    
    __tabs_name = {TAB_SETTINGS: _("Settings"),
                   TAB_SSL_OPTIONS: _("SSL options"),
                   TAB_SSH_TUNEL: _("SSH tunnel"),
                   TAB_STATISTCS: _("Statistics")
                   }
    
    __tabs = {MYSQL_TCP_IP: [TAB_SETTINGS, TAB_SSL_OPTIONS, TAB_STATISTCS],
              MYSQL_NAMED_PIPE: [TAB_SETTINGS, TAB_STATISTCS],
              MYSQL_SSH_TUNEL: [TAB_SETTINGS, TAB_SSH_TUNEL,TAB_STATISTCS]
              }
    
    __all_fields = [FIELD_TYPE, FIELD_ADDRESS, FIELD_USER, FIELD_PASSWORD,
                    FIELD_PROMPT, FIELD_PORT, FIELD_COMPRESSED, FIELD_DATABASES,
                    FIELD_STARTUP_SCRIPT
                    ]
    
    __fields = {MYSQL_TCP_IP: __all_fields,
                MYSQL_NAMED_PIPE: __all_fields,
                MYSQL_SSH_TUNEL: __all_fields
                }
    __fields[MYSQL_NAMED_PIPE].remove(FIELD_PORT)
    
    
    __label = {FIELD_TYPE: _("Network Type"),
               FIELD_ADDRESS: _("Hostname / IP"),
               FIELD_USER: _("User"),
               FIELD_PASSWORD: _("Passwrod"),
               FIELD_PROMPT: _("Prompt"),
               FIELD_PORT: _("Port"),
               FIELD_COMPRESSED: _("Compressed client/server protocol"),
               FIELD_DATABASES: _("Databases"),
               FIELD_STARTUP_SCRIPT: _("Startup script"),
               }
    
    @classmethod
    def get_tab_name(cls, tab):
        try:
            name = cls.__tabs_name[tab]
        except:
            name = ""
        else:
            return name
        
    @classmethod   
    def get_label(cls, field):
        try:
            label = cls.__label[field]
        except:
            label = ""
        else:
            return label
    
    @classmethod
    def get_dbs(cls):
        return cls.__all_bds
    
    """ 
    @return Type
    """
    @staticmethod
    def create_type(const_type):
        return Type(const_type)
    
    def __init__(self, type):
        self.__type = type
        
    def get_type(self):
        return self.__type
        
    def get_tabs(self):
        try:
            tabs = Type.__tabs[self.__type]
        except:
            return []
        else:
            return tabs
    
    def get_fields(self):
        try:
            fields = Type.__fields[self.__type]
        except:
            fields = []
        else:
            return fields
        
    def use_field(self, field):
        return field in self.get_fields()
    
    def get_port_default(self):
        return Type.__port_default[self.__type]
