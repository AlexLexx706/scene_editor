#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from editable_item import EditableItem
import resourses

class DynamicItem(EditableItem):
    def __init__(self, **kw_args):
        super(DynamicItem, self).__init__(**kw_args)
        self.set_enable_edit(False)
        self.set_attach_grid(False)
    
        self.update_timer = QtCore.QTimer()
        self.update_timer.start(1000/33)
        self.update_timer.timeout.connect(self.update_state)
    
    def update_state(self):
        '''Производит какойто процесс'''
        print "update_state"
