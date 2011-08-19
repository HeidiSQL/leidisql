# -*- coding: utf-8 -*-

from _pyio import __metaclass__
from abc import abstractmethod, ABCMeta



class ABCDatabases(object):

    __metaclass__ = ABCMeta

    @abstractmethod
    def get_databases_name(self):
        pass
