#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal

class ItemsModel(QtCore.QAbstractListModel):

    def __init__(self, scene):
        super(ItemsModel, self).__init__()
        self.__scene = scene
    
    def rowCount(self, parent):
        return len(self.__scene.items())
    
    def data(self, index, role):
        if not index.isValid():
            return QtCore.QVariant()
        
        if role == QtCore.Qt.DisplayRole:
            return self.__scene.items()[index.row()].get_name()
        elif role == QtCore.Qt.UserRole:
            return QtCore.QVariant(self.__scene.items()[index.row()])
        return QtCore.QVariant()
            
    
    def add_item(self, item):
        size = len(self.__scene.items())
        self.beginInsertRows(QtCore.QModelIndex(), size, size + 1)
        self.__scene.addItem(item)
        self.endInsertRows()

    def remove_item(self, item):
        index = self.__scene.items().index(item)
        self.beginRemoveRows(QtCore.QModelIndex(), index, index)
        self.__scene.removeItem(item)
        self.endRemoveRows()

    def clear_items(self):
        size = len(self.__scene.items())
        self.beginRemoveRows(QtCore.QModelIndex(), 0, size)
        self.__scene.clear()
        self.endRemoveRows()
    
    def get_index(self, item):
        index = self.__scene.items().index(item)
        return self.createIndex(index, 0)

    