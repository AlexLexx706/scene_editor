#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal
import resourses

class EditableItem(QtGui.QGraphicsItem):
    '''Базовый класс для редактируемых обьектов сцены, например как стена 
    '''
    CORNER_CHANGED = QtGui.QGraphicsItem.ItemTransformOriginPointHasChanged + 1
    
    def __init__(self, context_menu=None, rect=QtCore.QRectF(-20, -20, 40, 40)):
        super(EditableItem, self).__init__()
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges, True)
        
        self._context_menu = context_menu
        self._enable_edit = True
        self._rect = rect
        self._b_rect = self._rect
        self._shape_path = QtGui.QPainterPath()
        self._shape_path.addRect(self._rect)

        self._brush = QtGui.QBrush(QtGui.QImage(":/images/textures/brick.png"))
        self._pen = QtGui.QPen(QtCore.Qt.green, 1)

        self._edit_marker_brush = QtGui.QBrush(QtCore.Qt.black)
        self._edit_marker_size = 10
        self._edit_markers = None
        self._cur_edit_marker = None
    
    def is_enable_edit(self):
        return self._enable_edit
    
    def set_enable_edit(self, v):
        if self._enable_edit != v:
            self._enable_edit = v
            self._update_rect(rect, self.isSelected())

    def get_rect(self):
        return self._rect
        
    def set_rect(self, rect):
        if rect.width() < 0:
            rect.setWidth(0)

        if rect.height() < 0:
            rect.setHeight(0)

        if rect != self._rect:
            self._update_rect(rect, self.isSelected())
    
    def _update_rect(self, rect, is_selected):
        self.prepareGeometryChange()
        self._rect = rect

        if not is_selected or not self._enable_edit:
            self._b_rect = self._rect
            self._shape_path = QtGui.QPainterPath()
            self._shape_path.addRect(self._rect)
            self._edit_markers = None
        else:
            self._b_rect = QtCore.QRectF(self._rect.x() - self._edit_marker_size,
                                        self._rect.y() - self._edit_marker_size,
                                        self._rect.width() + self._edit_marker_size * 2,
                                        self._rect.height() + self._edit_marker_size * 2)
            
            self._edit_markers = [
                (QtCore.QRectF(self._b_rect.x(), self._b_rect.y(), self._edit_marker_size, self._edit_marker_size),
                    QtCore.QRectF.topLeft, QtCore.QRectF.setTopLeft),
                (QtCore.QRectF(self._b_rect.x() + self._b_rect.width() - self._edit_marker_size, self._b_rect.y(), self._edit_marker_size, self._edit_marker_size),
                    QtCore.QRectF.topRight, QtCore.QRectF.setTopRight),
                (QtCore.QRectF(self._b_rect.x(), self._b_rect.y() + self._b_rect.height() - self._edit_marker_size, self._edit_marker_size, self._edit_marker_size),
                    QtCore.QRectF.bottomLeft, QtCore.QRectF.setBottomLeft),
                (QtCore.QRectF(self._b_rect.x() + self._b_rect.width() - self._edit_marker_size, self._b_rect.y() + self._b_rect.height() - self._edit_marker_size, self._edit_marker_size, self._edit_marker_size), 
                    QtCore.QRectF.bottomRight, QtCore.QRectF.setBottomRight)
            ]

            self._shape_path = QtGui.QPainterPath()
            self._shape_path.addRect(self._rect)
            
            for d in self._edit_markers:
                self._shape_path.addRect(d[0])

        self.update()


    def boundingRect(self):
        return self._b_rect

    def shape(self):
        return self._shape_path
        
    def itemChange(self, change, value):
        '''Фильтр изменения состояний'''
        #изменения в выделении
        if change == QtGui.QGraphicsItem.ItemSelectedChange:
            self.prepareGeometryChange()
            self._update_rect(self._rect, value.toBool())
        #приведём координаты к сетке
        elif change == self.CORNER_CHANGED or change == QtGui.QGraphicsItem.ItemPositionChange:
            return QtCore.QVariant(self.mapFromScene(self.scene().grid_point(self.mapToScene(value.toPointF()))))
        return super(EditableItem, self).itemChange(change, value)
        
    def paint(self, painter, option, widget):
        painter.setPen(self._pen)
        painter.setBrush(self._brush)
        painter.drawRect(self._rect)
        
        #рисуем маркеры редактирования
        if self._edit_markers is not None:
            painter.setBrush(self._edit_marker_brush)
            painter.setPen(self._edit_marker_brush.color())
            
            for d in self._edit_markers:
                painter.drawRect(d[0])

        #выделение
        if self.isSelected():
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.setPen(QtGui.QPen(QtCore.Qt.red, 1, QtCore.Qt.DashLine))
            painter.drawRect(self._rect)
            
    def contextMenuEvent(self, event):
        if self._context_menu is None:
            event.ignore()
            return

        self.scene().clearSelection()
        self.setSelected(True)
        self._context_menu.exec_(event.screenPos())
    
    def mousePressEvent(self, event):
        if self._edit_markers is not None:
            for i, d in enumerate(self._edit_markers):
                if d[0].contains(event.pos()):
                    self.offset = d[1](self._rect) - event.pos()
                    self._cur_edit_marker = d
                    return

        self._cur_edit_marker = None
        super(EditableItem, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._cur_edit_marker is not None:
            r = QtCore.QRectF(self._rect)
            self._cur_edit_marker[2](r, self.itemChange(self.CORNER_CHANGED, QtCore.QVariant(event.pos() + self.offset)).toPointF())
            self.set_rect(r)
            return

        super(EditableItem, self).mouseMoveEvent(event)
