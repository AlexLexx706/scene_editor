#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import math

class GraphicScene(QtGui.QGraphicsScene):
    left_button_clicked = QtCore.pyqtSignal(QtGui.QGraphicsSceneMouseEvent)

    def __init__(self, parent=None):
        QtGui.QGraphicsScene.__init__(self, parent)

    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() == 1:
            self.left_button_clicked.emit(mouseEvent)
        QtGui.QGraphicsScene.mousePressEvent(self, mouseEvent)
