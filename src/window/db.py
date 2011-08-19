# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from _pyio import __metaclass__

class Db(object):
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def teste(self):
        pass