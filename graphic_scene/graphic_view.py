#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import math
import resourses

class GraphView(QtGui.QGraphicsView):
    left_button_clicked = QtCore.pyqtSignal(QtGui.QGraphicsSceneMouseEvent)
    
    def __init__(self, parent=None):
        '''Инициализация'''
        super(GraphView, self).__init__(parent)

    def wheelEvent(self, event):
        '''Реализация масштабирования'''
        self.scaleView(math.pow(2.0, -event.delta() / 240.0))

    def scaleView(self, scaleFactor):
        '''масштабирование'''
        factor = self.matrix().scale(scaleFactor, scaleFactor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()

        if factor < 0.07 or factor > 100:
            return
        self.scale(scaleFactor, scaleFactor)
    
    def drawBackground(self, painter, rect):
        self.scene().draw_backgroud_grid(self, painter, rect)
    
    def drawForeground(self, painter, rect):
        self.scene().draw_foreground_grid(self, painter, rect)
        
