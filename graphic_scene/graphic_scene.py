#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import math

class GraphicScene(QtGui.QGraphicsScene):
    left_button_clicked = QtCore.pyqtSignal(QtGui.QGraphicsSceneMouseEvent)
    GRID_SIZE = 20

    GRID_PEN = QtGui.QPen(QtGui.QBrush(QtCore.Qt.black), 1)
    GRID_PEN.setCosmetic(True)

    GRID_PEN_CENTER = QtGui.QPen(QtGui.QBrush(QtCore.Qt.red), 2)
    GRID_PEN_CENTER.setCosmetic(True)

    def __init__(self, parent=None):
        QtGui.QGraphicsScene.__init__(self, parent)

    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() == 1:
            self.left_button_clicked.emit(mouseEvent)
        QtGui.QGraphicsScene.mousePressEvent(self, mouseEvent)

    def drawBackground__(self, painter, rect):
        painter.setPen(self.GRID_PEN)

        greed_step = rect.width() / painter.window().width() * self.GRID_SIZE
        left = rect.left() - math.frexp(rect.left() / greed_step)[0] * greed_step
        #greed_step = self.GRID_SIZE
        #left = rect.left() - int(rect.left()) % greed_step

        while left < rect.right():
            if left == 0:
                painter.save()
                painter.setPen(self.GRID_PEN_CENTER)
                painter.drawLine(left, rect.top(), left, rect.bottom())
                painter.restore()
            else:
                painter.drawLine(left, rect.top(), left, rect.bottom())
            painter.drawText(left, 0, str(left))
            left += greed_step

        greed_step = rect.height() / painter.window().height() * self.GRID_SIZE
        top = rect.top() - math.frexp(rect.top() / greed_step)[0] * greed_step
        #greed_step = self.GRID_SIZE
        #top = rect.top() - int(rect.top()) % greed_step

        while top < rect.bottom():
            if top == 0:
                painter.save()
                painter.setPen(self.GRID_PEN_CENTER)
                painter.drawLine(rect.left(), top, rect.right(), top)
                painter.restore()
            else:
                painter.drawLine(rect.left(), top, rect.right(), top)
            painter.drawText(0, top, str(top))
            top += greed_step
