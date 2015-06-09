#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from dynamic_Item import DynamicItem
import resourses
import math
import time

class ShitItem(DynamicItem):
    def __init__(self, **kw_args):
        super(ShitItem, self).__init__(image=QtGui.QImage(":/images/objects/shit.png"), **kw_args)

    @staticmethod
    def item_type():
        return "ShitItem"

    @staticmethod
    def deserialize(desc):
        return ShitItem(**desc)

DynamicItem.FACTORY_MAP[ShitItem.item_type()] = ShitItem.deserialize
        
