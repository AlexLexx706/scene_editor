#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from editable_item import EditableItem
import resourses

class BrickItem(EditableItem):
    def __init__(self, **kw_args):
        super(BrickItem, self).__init__(**kw_args)
        self._brush = QtGui.QBrush(QtGui.QImage(":/images/textures/brick.png"))
        self._pen = QtGui.QPen(QtCore.Qt.green, 1)

    def paint_item(self, painter, option, widget):
        painter.setPen(self._pen)
        painter.setBrush(self._brush)
        painter.drawRect(self.get_rect())