#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
from scene_editor.items.base_item import BaseItem
import scene_editor.resourses


class BrickItem(BaseItem):
    def __init__(self, **kw_args):
        super(BrickItem, self).__init__(**kw_args)
        self._brush = QtGui.QBrush(QtGui.QImage(":/images/textures/brick.png"))
        self._pen = QtGui.QPen(QtCore.Qt.green, 1)

    def paint_item(self, painter, option, widget):
        painter.setPen(self._pen)
        painter.setBrush(self._brush)
        painter.drawRect(self.get_rect())

    @staticmethod
    def item_type():
        return "BrickItem"

    @staticmethod
    def deserialize(desc):
        return BrickItem(**desc)


BaseItem.FACTORY_MAP[BrickItem.item_type()] = BrickItem.deserialize