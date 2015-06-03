#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import math

class GraphView(QtGui.QGraphicsView):
    def __init__(self, parent=None):
        super(GraphView, self).__init__(parent)
        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QtGui.QGraphicsView.BoundingRectViewportUpdate)
        self.setRenderHint(QtGui.QPainter.Antialiasing)

        #self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        #self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        #self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)

    def wheelEvent(self, event):
        self.scaleView(math.pow(2.0, -event.delta() / 240.0))

    def scaleView(self, scaleFactor):
        factor = self.matrix().scale(scaleFactor, scaleFactor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()

        if factor < 0.07 or factor > 100:
            return
        self.scale(scaleFactor, scaleFactor)
    
    # def mouseMoveEvent(self, event):
        # if event.buttons() & QtCore.Qt.MidButton:
            # d = (event.pos() - self.s_pos) * 100
            # self.s_pos = event.pos()
            # #d = self.mapFromScene(event.pos() - self.s_pos)
            # print d.x(), d.y()
            # self.translate(d.x(), d.y())
        # super(GraphView, self).mouseMoveEvent(event)
    
    # def mousePressEvent(self, event):
        # if event.button() == QtCore.Qt.MidButton:
            # self.s_pos = event.pos()
        # super(GraphView, self).mousePressEvent(event)