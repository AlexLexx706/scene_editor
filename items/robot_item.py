#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from dynamic_Item import DynamicItem
import resourses
import math
import time

class ModelInterface:
    def __init__(self, model_id):
        self.model_id = model_id

    def send_cmd(self, cmd, params=None):
        if self.model_id == 0:
            if cmd == "get_angle":
                return math.cos(time.time())

class RobotItem(DynamicItem):
    def __init__(self, **kw_args):
        super(RobotItem, self).__init__(**kw_args)
        self._image = QtGui.QImage(":/images/textures/bulldozer-top.png")
        self._source = QtCore.QRectF(0.0, 0.0, self._image.width(), self._image.height())
        self.model_interface = ModelInterface(0)

    def paint_item(self, painter, option, widget):
        painter.drawImage(self.get_rect(), self._image, self._source)
    
    def update_state(self):
        '''Производит какойто процесс'''
        self.rotate(self.model_interface.send_cmd("get_angle"))
        
