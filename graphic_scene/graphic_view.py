#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import math
import resourses

class GraphView(QtGui.QGraphicsView):
    left_button_clicked = QtCore.pyqtSignal(QtGui.QGraphicsSceneMouseEvent)
    
    #настройки сетки
    GRID_STEP = 10
    GRID_PIXEL_STEP = 40
    GRID_PEN = QtGui.QPen(QtGui.QBrush(QtCore.Qt.black), 1)
    GRID_PEN.setCosmetic(True)
    GRID_CENTER_PEN = QtGui.QPen(QtGui.QBrush(QtCore.Qt.red), 2)
    GRID_CENTER_PEN.setCosmetic(True)
    GRID_FONT = QtGui.QFont("Times", 10, True)
    
    GRID_BACKGROUD_BRUSH = QtGui.QBrush(QtCore.Qt.white)

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
        '''Рисует сетку'''
        rect = QtCore.QRectF(rect.x() - self.GRID_PIXEL_STEP, rect.y() - self.GRID_PIXEL_STEP,
                        rect.width() + self.GRID_PIXEL_STEP * 2, rect.height() + self.GRID_PIXEL_STEP * 2)

        scene_rect = self.mapToScene(self.viewport().geometry()).boundingRect()
        
        #расчёт шага по горизонтали
        greed_step = scene_rect.width() / painter.window().width() * self.GRID_PIXEL_STEP
        greed_step -= math.modf(greed_step / self.GRID_STEP)[0] * self.GRID_STEP

        if greed_step < self.GRID_STEP:
            greed_step = self.GRID_STEP

        left = rect.left() - math.modf(rect.left() / greed_step)[0] * greed_step

        text_list = []
        painter.setPen(self.GRID_PEN)
        
        while left <= rect.right():
            if int(left) == 0:
                painter.save()
                painter.setPen(self.GRID_CENTER_PEN)
                painter.drawLine(left, rect.top(), left, rect.bottom())
                painter.restore()
            else:
                painter.drawLine(left, rect.top(), left, rect.bottom())

                p = self.mapFromScene(left, 0)
                p.setY(p.y() - 2)
                text_list.append((p, left))

            left += greed_step

        #расчёт шага по вертикали
        greed_step = scene_rect.height() / painter.window().height() * self.GRID_PIXEL_STEP
        greed_step -= math.modf(greed_step / self.GRID_STEP)[0] * self.GRID_STEP

        if greed_step < self.GRID_STEP:
            greed_step = self.GRID_STEP

        top = rect.top() - math.modf(rect.top() / greed_step)[0] * greed_step

        while top < rect.bottom():
            if int(top) == 0:
                painter.save()
                painter.setPen(self.GRID_CENTER_PEN)
                painter.drawLine(rect.left(), top, rect.right(), top)
                painter.restore()
            else:
                painter.drawLine(rect.left(), top, rect.right(), top)
            
                p = self.mapFromScene(0, top)
                p.setX(p.x() + 2)
                text_list.append((p, top))

            top += greed_step

        #отображение не масштабируемого текста
        painter.resetTransform()
        painter.setFont(self.GRID_FONT)
        
        for pos, value in text_list:
            painter.drawText(pos, str(int(value)))
        
