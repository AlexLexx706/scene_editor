#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
import math


class GraphicScene(QtGui.QGraphicsScene):
    left_button_clicked = QtCore.pyqtSignal(QtGui.QGraphicsSceneMouseEvent)

    # настройки сетки
    GRID_STEP = 10.0
    GRID_PIXEL_STEP = 40.0
    GRID_PEN = QtGui.QPen(QtGui.QBrush(QtCore.Qt.black), 1)
    GRID_PEN.setCosmetic(True)
    GRID_CENTER_PEN = QtGui.QPen(QtGui.QBrush(QtCore.Qt.blue), 2)
    GRID_CENTER_PEN.setCosmetic(True)
    GRID_FONT = QtGui.QFont("Times", 11, True)
    GRID_FONT_COLOR = QtGui.QPen(QtCore.Qt.black)
    GRID_BACKGROUD_BRUSH = QtGui.QBrush(QtCore.Qt.white)
    RULER_WIDTH = 20
    RULER_BRUSH = QtGui.QBrush(QtCore.Qt.white)
    RULER_PEN = QtGui.QPen(QtGui.QBrush(QtCore.Qt.black), 1)

    def __init__(self, parent=None):
        QtGui.QGraphicsScene.__init__(self, parent)
        self.use_grid_point = True

    def mousePressEvent(self, mouseEvent):
        '''Генерит событие нажата кнопка мыши'''
        if mouseEvent.button() == 1:
            self.left_button_clicked.emit(mouseEvent)
        QtGui.QGraphicsScene.mousePressEvent(self, mouseEvent)

    def grid_point(self, scene_pos):
        """
            Возвращает координаты прикреплённые к сетке,
            в зависимости от флага use_grid_point
        """
        if not self.use_grid_point:
            return scene_pos

        res = QtCore.QPointF()

        # определим остаток от деления
        x_mod = abs(math.modf(scene_pos.x() / self.GRID_STEP)[0])
        x_sign = -1.0 if scene_pos.x() < 0.0 else 1.0

        if x_mod > 0.5:
            res.setX((
                abs(scene_pos.x()) + (1.0 - x_mod) * self.GRID_STEP) * x_sign)
        else:
            res.setX((abs(scene_pos.x()) - x_mod * self.GRID_STEP) * x_sign)

        y_mod = abs(math.modf(scene_pos.y() / self.GRID_STEP)[0])
        y_sign = -1.0 if scene_pos.y() < 0.0 else 1.0

        if y_mod > 0.5:
            res.setY(
                (abs(scene_pos.y()) + (1.0 - y_mod) * self.GRID_STEP) * y_sign)
        else:
            res.setY((abs(scene_pos.y()) - y_mod * self.GRID_STEP) * y_sign)

        return res

    def scene_grid_steps(self, view):
        '''Получить шаг с учётом масштабирования в координатах сцены'''
        scene_rect = view.mapToScene(view.viewport().geometry()).boundingRect()

        x_step = (self.GRID_PIXEL_STEP / view.viewport().width()) * \
            scene_rect.width()
        x_step -= math.modf(x_step / self.GRID_STEP)[0] * self.GRID_STEP

        y_step = (self.GRID_PIXEL_STEP / view.viewport().height()) * \
            scene_rect.height()
        y_step -= math.modf(y_step / self.GRID_STEP)[0] * self.GRID_STEP

        return ((x_step if x_step > self.GRID_STEP else self.GRID_STEP, y_step if y_step > self.GRID_STEP else self.GRID_STEP), scene_rect)

    def draw_backgroud_grid(self, view, painter, rect):
        '''Рисует сетку на заднике view'''
        grid_step, _scene_rect = self.scene_grid_steps(view)

        left = rect.left() - math.modf(rect.left() /
                                       grid_step[0])[0] * grid_step[0]
        painter.setPen(self.GRID_PEN)

        while left <= rect.right():
            painter.drawLine(left, rect.top(), left, rect.bottom())
            left += grid_step[0]

        # расчёт шага по вертикали
        top = rect.top() - math.modf(rect.top() /
                                     grid_step[1])[0] * grid_step[1]

        while top < rect.bottom():
            painter.drawLine(rect.left(), top, rect.right(), top)
            top += grid_step[1]

    def draw_foreground_grid(self, view, painter, rect):
        '''Рисуем линейку на переднем плане'''
        grid_step, rect = self.scene_grid_steps(view)
        left = rect.left() - math.modf(rect.left() /
                                       grid_step[0])[0] * grid_step[0]
        width = view.viewport().width()
        height = view.viewport().height()

        painter.resetTransform()
        #painter.setClipRect(QtCore.QRect(0,0, width, height))

        painter.setPen(self.RULER_PEN)
        painter.setBrush(self.RULER_BRUSH)
        painter.drawRect(0, 0, width, self.RULER_WIDTH)

        painter.setFont(self.GRID_FONT)
        painter.setPen(self.GRID_FONT_COLOR)
        h = (self.RULER_WIDTH + QtGui.QFontMetrics(self.GRID_FONT).height()) / 2

        while left <= rect.right():
            painter.drawText(view.mapFromScene(left, 0).x(), h, str(int(left)))
            left += grid_step[0]

        painter.setPen(self.RULER_PEN)
        painter.setBrush(self.RULER_BRUSH)
        ruler_rect = QtCore.QRectF(
            0, self.RULER_WIDTH, self.RULER_WIDTH, height - self.RULER_WIDTH)
        painter.setClipRect(ruler_rect, QtCore.Qt.UniteClip)
        painter.drawRect(ruler_rect)

        painter.setFont(self.GRID_FONT)
        painter.setPen(self.GRID_FONT_COLOR)

        top = rect.top() - math.modf(rect.top() /
                                     grid_step[1])[0] * grid_step[1]
        offset = self.RULER_WIDTH / 2.0 - \
            QtGui.QFontMetrics(self.GRID_FONT).height() / 2.0
        #offset = 100
        painter.translate(QtCore.QPointF(offset, 0))
        painter.rotate(90)

        while top < rect.bottom():
            painter.drawText(view.mapFromScene(0, top).y(), 0, str(int(top)))
            top += grid_step[1]
