#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import math
import resourses
import json

class GraphView(QtGui.QGraphicsView):
    drop_new_object = QtCore.pyqtSignal(object)
    
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
        return 
        self.scene().draw_foreground_grid(self, painter, rect)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/scene-item-type"):
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/scene-item-type"):
            event.acceptProposedAction()

    def dropEvent(self, event):
        if event.proposedAction() == QtCore.Qt.MoveAction:
            event.acceptProposedAction()
            data = json.loads(str(event.mimeData().data("application/scene-item-type")))
            data["scene_pos"] = self.mapToScene(event.pos())
            self.drop_new_object.emit(data)