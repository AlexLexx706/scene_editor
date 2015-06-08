#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from items.brick_item import BrickItem
from items.robot_item import RobotItem
from items_model.items_model import ItemsModel
from graphic_scene.graphic_scene import GraphicScene
import resourses
import logging

logger = logging.getLogger(__name__)


class MainWindow(QtGui.QMainWindow):
    add_line = pyqtSignal(str)
    
    BORDER_ID = 0
    ROBOT_ID = 1
    SHIT_ID = 2
    STORAGE_ID = 3
    GARAGE_ID = 4
    
    def __init__(self, parent=None):
        super(QtGui.QWidget, self).__init__(parent)
        uic.loadUi("main_window.ui", self)
        self.settings = QtCore.QSettings("AlexLexx", "larm_scene_editor")

        self.scene = GraphicScene()
        self.scene.selectionChanged.connect(self.on_scene_selectionChanged)
        self.graphicsView.setScene(self.scene)
        self.splitter.setSizes([1000, 100])

        self.items_model = ItemsModel()
        self.listView_objects.setModel(self.items_model)
        self.listView_objects.selectionModel().selectionChanged.connect(self.on_listView_objects_selectionChanged)
        
        #соадим группу кнопок создания обьектов
        self.buttonGroup = QtGui.QButtonGroup()
        self.buttonGroup.setExclusive(False)
        
        self.toolButton.scene_object_type = self.BORDER_ID
        self.buttonGroup.addButton(self.toolButton)
        
        self.toolButton_2.scene_object_type = self.ROBOT_ID
        self.buttonGroup.addButton(self.toolButton_2)
        
        self.toolButton_3.scene_object_type = self.SHIT_ID
        self.buttonGroup.addButton(self.toolButton_3)
        
        self.toolButton_4.scene_object_type = self.STORAGE_ID
        self.buttonGroup.addButton(self.toolButton_4)
        
        self.toolButton_5.scene_object_type = self.GARAGE_ID
        self.buttonGroup.addButton(self.toolButton_5)
       
        self.buttonGroup.buttonClicked.connect(self.buttonGroupClicked)
        self.graphicsView.drop_new_object.connect(self.drop_new_object)
        
        self.states_group = QtGui.QActionGroup(self)
        self.states_group.addAction(self.action_select_state)
        self.states_group.addAction(self.action_drag_scene)
        self.states_group.triggered.connect(self.on_state_changed)
    
    @pyqtSlot(QtGui.QAction)
    def on_state_changed(self, action):
        if action == self.action_select_state:
            self.graphicsView.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        elif action == self.action_drag_scene:
            self.graphicsView.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)

    @pyqtSlot(QtGui.QAbstractButton)
    def buttonGroupClicked(self, clicked_button):
        for button in self.buttonGroup.buttons():
            if clicked_button != button:
                button.setChecked(False)
    
    @pyqtSlot('bool')
    def on_action_bring_to_front_triggered(self, checked):
        if not self.scene.selectedItems():
            return

        selectedItem = self.scene.selectedItems()[0]
        overlapItems = selectedItem.collidingItems()

        zValue = 0
        for item in overlapItems:
            if item.zValue() >= zValue:
                zValue = item.zValue() + 0.1
        selectedItem.setZValue(zValue)

    @pyqtSlot('bool')
    def on_action_send_to_back_triggered(self, checked):
        if not self.scene.selectedItems():
            return

        selectedItem = self.scene.selectedItems()[0]
        overlapItems = selectedItem.collidingItems()

        zValue = 0
        for item in overlapItems:
            if item.zValue() <= zValue:
                zValue = item.zValue() - 0.1
        selectedItem.setZValue(zValue)

    def drop_new_object(self, desc):
        if desc["type"] != -1:
            self.scene.clearSelection()

            #Сделаем стену
            if desc["type"] == self.BORDER_ID:
                item = BrickItem(context_menu = self.menu_elements, rect=QtCore.QRectF(-20, -20, 40, 40))
                item.setData(0, {"name": u"Стена"})
                self.scene.addItem(item)
                item.setPos(self.scene.grid_point(desc["scene_pos"]))
                self.items_model.add_object(item)
            elif desc["type"] == self.ROBOT_ID:
                item = RobotItem(context_menu = self.menu_elements, rect=QtCore.QRectF(-20, -20, 40, 40))
                item.setData(0, {"name": u"Бендер"})
                self.scene.addItem(item)
                item.setPos(self.scene.grid_point(desc["scene_pos"]))
                self.items_model.add_object(item)
                

    @pyqtSlot('const QItemSelection &', 'const QItemSelection &')
    def on_listView_objects_selectionChanged(self, selected, deselected):
        self.scene.blockSignals(True)

        self.scene.clearSelection()

        for index in self.listView_objects.selectionModel().selectedIndexes():
            obj = self.items_model.itemFromIndex(index).data().toPyObject()
            obj.setSelected(True)
            self.update_obj_capacity_view(obj)

        self.scene.blockSignals(False)

    def update_obj_capacity_view(self, obj):
        self.doubleSpinBox_pos_x.setValue(obj.pos().x())
        self.doubleSpinBox_pos_y.setValue(obj.pos().y())


    @pyqtSlot('double')
    def on_scene_selectionChanged(self):
        items = self.scene.selectedItems()

        if len(items) == 0:
            self.listView_objects.clearSelection()
            return

        self.listView_objects.setCurrentIndex(self.items_model.get_model_index(items[0]))

    @pyqtSlot('bool')
    def on_action_remove_triggered(self, checked):
        for item in self.scene.selectedItems():
            self.scene.removeItem(item)
            self.items_model.remove_obj(item)

if __name__ == '__main__':
    import sys
    import logging
    
    logging.basicConfig(format='%(levelname)s %(name)s::%(funcName)s%(message)s', level=logging.DEBUG)
    #logging.getLogger("PyQt4").setLevel(logging.INFO)

    app = QtGui.QApplication(sys.argv)
    widget = MainWindow()
    app.installEventFilter(widget)
    widget.show()
    app.exec_()
