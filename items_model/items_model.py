#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal

class ItemsModel(QtGui.QStandardItemModel):

    def __init__(self, contextMenu=None):
        QtGui.QStandardItemModel.__init__(self)
        self.object_map = {}
    
    def add_object(self, obj):
        root = self.invisibleRootItem()
        item = QtGui.QStandardItem(obj.data(0).toPyObject()[QtCore.QString("name")])
        item.setData(obj)
        root.appendRow(item)
        self.object_map[obj] = item

    def remove_obj(self, obj):
        self.invisibleRootItem().removeRow(self.object_map[obj].row())
        del self.object_map[obj]

    def get_model_index(self, obj):
        return self.object_map[obj].index()