#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal
import resourses

class BaseItem(QtGui.QGraphicsItem):
    '''Базовый класс для редактируемых обьектов сцены, например как стена '''
    CORNER_CHANGED = QtGui.QGraphicsItem.ItemTransformOriginPointHasChanged + 1
    FACTORY_MAP = {}

    def __init__(self, **kw_args):
        '''Инициализация базового класса, возможные параметры:
           context_menu - QMenu, ссылка на обьект контекстного меню
           rect - QRectF, размеры обьекта
           edit_marker_size - int - размеры маркера редактирования
           attach_grid - bool - прилипать к сетке сцены
           editable - bool - разрешение редактирования
           pos - QPaintF - позиция
           name - string - имя обьекта
        '''

        self.__attach_grid = kw_args["attach_grid"] if "attach_grid" in kw_args else True
        super(BaseItem, self).__init__()
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges, True)
        
        self.__context_menu = kw_args["context_menu"] if "context_menu" in kw_args else None
        self.__rect = (kw_args["rect"] if isinstance(kw_args["rect"], QtCore.QRectF) else QtCore.QRectF(kw_args["rect"][0], kw_args["rect"][1], kw_args["rect"][2], kw_args["rect"][3]) )\
            if "rect" in kw_args else QtCore.QRectF(-20, -20, 40, 40)
        self.__editable = kw_args["editable"] if "editable" in kw_args else True
        self.__edit_marker_size = kw_args["edit_marker_size"] if "edit_marker_size" in kw_args else 10
        
        #self.setPos((kw_args["pos"] if isinstance(kw_args["pos"], QtCore.QPointF) else QtCore.QPointF(kw_args["pos"][0], kw_args["pos"][1]))\
        #    if "pos" in kw_args else QtCore.QPointF(0.0, 0.0))

        self.__name = kw_args["name"] if "name" in kw_args else "unknown"

        self.__b_rect = self.__rect
        self.__shape_path = QtGui.QPainterPath()
        self.__shape_path.addRect(self.__rect)

        self.__edit_marker_brush = QtGui.QBrush(QtCore.Qt.black)
        self.__edit_markers = None
        self.__cur_edit_marker = None
    
    def get_name(self):
        return self.__name
    
    def set_name(self, name):
        self.__name = name

    @staticmethod
    def item_type():
        return "BaseItem"

    def serialize(self):
        return {"type": self.item_type(),
                "pos": (self.pos().x(), self.pos().y()),
                "rect": (self.get_rect().x(), self.get_rect().y(), self.get_rect().width(), self.get_rect().height()),
                "edit_marker_size": self.__edit_marker_size,
                "attach_grid": self.is_attach_grid(),
                "editable": self.is_editable(),
                "name": self.get_name()}

    @staticmethod
    def deserialize(desc):
        return BaseItem(**desc)
   
    @staticmethod
    def create(desc):
        return BaseItem.FACTORY_MAP[desc["type"]](desc)

    def is_attach_grid(self):
        return self.__attach_grid
    
    def set_attach_grid(self, v):
        self.__attach_grid =  v
    
    def is_editable(self):
        return self.__editable
    
    def set_editable(self, v):
        if self.__editable != v:
            self.__editable = v
            self.__update_rect(self.__rect, self.isSelected())

    def get_rect(self):
        return self.__rect
        
    def set_rect(self, rect):
        if rect.width() < 0:
            rect.setWidth(0)

        if rect.height() < 0:
            rect.setHeight(0)

        if rect != self.__rect:
            self.__update_rect(rect, self.isSelected())
    
    def boundingRect(self):
        return self.__b_rect

    def shape(self):
        return self.__shape_path
        
    def itemChange(self, change, value):
        '''Фильтр изменения состояний'''
        #изменения в выделении
        if change == QtGui.QGraphicsItem.ItemSelectedChange:
            self.prepareGeometryChange()
            self.__update_rect(self.__rect, value.toBool())
        #приведём координаты к сетке
        elif self.__attach_grid and self.scene() and  (change == self.CORNER_CHANGED or change == QtGui.QGraphicsItem.ItemPositionChange):
            return QtCore.QVariant(self.mapFromScene(self.scene().grid_point(self.mapToScene(value.toPointF()))))
        return super(BaseItem, self).itemChange(change, value)
    
    def paint_item(self, painter, option, widget):
        painter.setPen(QtGui.QPen(QtCore.Qt.green, 1))
        painter.setBrush(QtGui.QBrush(QtCore.Qt.green))
        painter.drawRect(self.__rect)
    
    def paint(self, painter, option, widget):
        self.paint_item(painter, option, widget)
        
        #рисуем маркеры редактирования
        if self.__edit_markers is not None:
            painter.setBrush(self.__edit_marker_brush)
            painter.setPen(self.__edit_marker_brush.color())
            
            for d in self.__edit_markers:
                painter.drawRect(d[0])

        #выделение
        if self.isSelected():
            painter.setBrush(QtCore.Qt.NoBrush)
            painter.setPen(QtGui.QPen(QtCore.Qt.red, 1, QtCore.Qt.DashLine))
            painter.drawRect(self.__rect)
            
    def contextMenuEvent(self, event):
        if self.__context_menu is None:
            event.ignore()
            return
        self.scene().clearSelection()
        self.setSelected(True)
        self.__context_menu.exec_(event.screenPos())
    
    def mousePressEvent(self, event):
        if self.__edit_markers is not None:
            for i, d in enumerate(self.__edit_markers):
                if d[0].contains(event.pos()):
                    self.offset = d[1](self.__rect) - event.pos()
                    self.__cur_edit_marker = d
                    return

        self.__cur_edit_marker = None
        super(BaseItem, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.__cur_edit_marker is not None:
            r = QtCore.QRectF(self.__rect)
            self.__cur_edit_marker[2](r, self.itemChange(self.CORNER_CHANGED, QtCore.QVariant(event.pos() + self.offset)).toPointF())
            self.set_rect(r)
            return

        super(BaseItem, self).mouseMoveEvent(event)

    def __update_rect(self, rect, is_selected):
        self.prepareGeometryChange()
        self.__rect = rect

        if not is_selected or not self.__editable:
            self.__b_rect = self.__rect
            self.__shape_path = QtGui.QPainterPath()
            self.__shape_path.addRect(self.__rect)
            self.__edit_markers = None
        else:
            self.__b_rect = QtCore.QRectF(self.__rect.x() - self.__edit_marker_size,
                                        self.__rect.y() - self.__edit_marker_size,
                                        self.__rect.width() + self.__edit_marker_size * 2,
                                        self.__rect.height() + self.__edit_marker_size * 2)
            
            self.__edit_markers = [
                (QtCore.QRectF(self.__b_rect.x(), self.__b_rect.y(), self.__edit_marker_size, self.__edit_marker_size),
                    QtCore.QRectF.topLeft, QtCore.QRectF.setTopLeft),
                (QtCore.QRectF(self.__b_rect.x() + self.__b_rect.width() - self.__edit_marker_size, self.__b_rect.y(), self.__edit_marker_size, self.__edit_marker_size),
                    QtCore.QRectF.topRight, QtCore.QRectF.setTopRight),
                (QtCore.QRectF(self.__b_rect.x(), self.__b_rect.y() + self.__b_rect.height() - self.__edit_marker_size, self.__edit_marker_size, self.__edit_marker_size),
                    QtCore.QRectF.bottomLeft, QtCore.QRectF.setBottomLeft),
                (QtCore.QRectF(self.__b_rect.x() + self.__b_rect.width() - self.__edit_marker_size, self.__b_rect.y() + self.__b_rect.height() - self.__edit_marker_size, self.__edit_marker_size, self.__edit_marker_size), 
                    QtCore.QRectF.bottomRight, QtCore.QRectF.setBottomRight)
            ]

            self.__shape_path = QtGui.QPainterPath()
            self.__shape_path.addRect(self.__rect)
            
            for d in self.__edit_markers:
                self.__shape_path.addRect(d[0])

        self.update()

BaseItem.FACTORY_MAP[BaseItem.item_type()] = BaseItem.deserialize
        