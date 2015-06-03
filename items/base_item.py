#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal

class BaseItem(QtGui.QGraphicsRectItem):
    NO_MOVE = -1
    MOVE_TOP_LEFT = 0
    MOVE_BOTTOM_RIGHT = 1
    
    def __init__(self, contextMenu=None, rect = QtCore.QRectF(0,0,50,50)):
        QtGui.QGraphicsRectItem.__init__(self)
        self.contextMenu = contextMenu
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        #self.setFlag(QtGui.QGraphicsItem.ItemIgnoresTransformations, True)
        self.setRect(rect)
        self.setBrush(QtGui.QBrush(QtCore.Qt.red, QtCore.Qt.FDiagPattern))
        self.setPen(QtGui.QPen(QtCore.Qt.green, 3))

        self.border_brush = QtGui.QBrush(QtCore.Qt.red)
        self.move_border_flag = self.NO_MOVE
        self.select_border_size = 8
    
    def set_width(self, w):
        r = self.rect()
        r.setWidth(w)
        self.rect(r)

    def set_height(self, h):
        r = self.rect()
        r.setheight(h)
        self.rect(r)

    def contextMenuEvent(self, event):
        if self.contextMenu is None:
            event.ignore()
            return

        self.scene().clearSelection()
        self.setSelected(True)
        self.contextMenu.exec_(event.screenPos())
    
    def mouseMoveEvent(self, event):
        if self.move_border_flag == self.MOVE_TOP_LEFT:
            r = self.rect()
            r.setTopLeft(event.pos() + self.offset)
            self.setRect(r)
            return
        elif self.move_border_flag == self.MOVE_BOTTOM_RIGHT:
            r = self.rect()
            r.setBottomRight(event.pos() + self.offset)
            self.setRect(r)
            return
        QtGui.QGraphicsRectItem.mouseMoveEvent(self, event)

    def mousePressEvent(self, event):
        r = self.rect()
        if QtCore.QRectF(r.x(), r.y(), self.select_border_size, self.select_border_size).contains(event.pos()):
            self.move_border_flag = self.MOVE_TOP_LEFT
            self.offset = r.topLeft() - event.pos()
            return
        elif QtCore.QRectF(r.x() + r.width() - self.select_border_size, r.y() + r.height() - self.select_border_size,
            self.select_border_size, self.select_border_size).contains(event.pos()):
            self.move_border_flag = self.MOVE_BOTTOM_RIGHT
            self.offset = r.bottomRight() - event.pos()
            return
        self.move_border_flag = self.NO_MOVE
        self.update()
        QtGui.QGraphicsRectItem.mousePressEvent(self, event)
    
    def mouseReleaseEvent(self, event):
        self.move_border_flag = self.NO_MOVE
        self.update()
        QtGui.QGraphicsRectItem.mouseReleaseEvent(self, event)
    
    def paint(self, painter, option, widget):
        super(BaseItem, self).paint(painter, option, widget)
        
        if self.move_border_flag == self.MOVE_TOP_LEFT:
            painter.setBrush(self.border_brush)
            painter.setPen(self.border_brush.color())
            p = self.rect().topLeft()
            painter.drawRect(p.x(), p.y(), self.select_border_size, self.select_border_size)
        elif self.move_border_flag == self.MOVE_BOTTOM_RIGHT:
            painter.setBrush(self.border_brush)
            painter.setPen(self.border_brush.color())
            p = self.rect().bottomRight() - QtCore.QPointF(self.select_border_size, self.select_border_size)
            painter.drawRect(p.x(), p.y(), self.select_border_size, self.select_border_size)