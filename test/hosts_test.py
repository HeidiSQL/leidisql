# -*- coding: utf-8 -*-

import unittest
import os

import hosts
from hosts import Type
from hosts import Host
from hosts import List

class HostsTest(unittest.TestCase):
    
    def setUp(self):
        try:
            os.remove(List.DB)
        except OSError:
            pass
    
    def test_type(self):
        typeMysqlTcpIp = Type.create_type(Type.MYSQL_TCP_IP);
        self.assertEqual([Type.TAB_SETTINGS, Type.TAB_SSL_OPTIONS, Type.TAB_STATISTCS], typeMysqlTcpIp.get_tabs())
        
    
    def test_host(self):
        type = Type.create_type(Type.MYSQL_TCP_IP);
        host = hosts.Host("Teste", type)
        host.address = "localhost"
        host.user = "root"
        host.password = "123"
        host.port = "3306"
        
        self.assertEqual("Teste", host.name)
        self.assertEqual(type, host.type)
        self.assertEqual("localhost", host.address)
        self.assertEqual("root", host.user)
        self.assertEqual("123", host.password)
        self.assertEqual("3306", host.port)
        
        try:
            host = hosts.Host(None, type)
        except hosts.ExceptHostNameInvalid:
            expr = True
        else:
            expr = False
            
        self.assertTrue(expr)
        
        
        
    def test_list(self):
        type = Type.create_type(Type.MYSQL_TCP_IP);
        hostsNames = ["teste", "teste2"]
        host = Host(hostsNames[0], type)
        host2 = Host(hostsNames[1], type)
        
        listHost = List()
        listHost.add(host)
        listHost.add(host2)
        
        i = 0
        for v in listHost.iteritems():
            self.assertEquals(hostsNames[i], v.name)
            i += 1
            
        try:
            listHost.add(host2)
        except hosts.ExceptHostNameExist:
            expr = True
        else:
            expr = False
            
        self.assertTrue(expr)
        
        
if __name__ == '__main__':
    unittest.main()