#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from items.base_item import BaseItem
from items.brick_item import BrickItem
from items.robot_item import RobotItem
from items.shit_item import ShitItem
from items_model.items_model import ItemsModel
from graphic_scene.graphic_scene import GraphicScene
import resourses
import logging
import json

logger = logging.getLogger(__name__)


class MainWindow(QtGui.QMainWindow):
    add_line = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super(QtGui.QWidget, self).__init__(parent)
        uic.loadUi("main_window.ui", self)
        self.settings = QtCore.QSettings("AlexLexx", "larm_scene_editor")

        self.scene = GraphicScene()
        self.scene.selectionChanged.connect(self.on_scene_selectionChanged)
        self.graphicsView.setScene(self.scene)
        self.splitter.setSizes([1000, 100])

        self.items_model = ItemsModel(self.scene)
        self.listView_objects.setModel(self.items_model)
        self.listView_objects.selectionModel().selectionChanged.connect(self.on_listView_objects_selectionChanged)
        
        #соадим группу кнопок создания обьектов
        self.buttonGroup = QtGui.QButtonGroup()
        self.buttonGroup.setExclusive(False)
        
        self.toolButton.scene_object_type = BrickItem.item_type()
        self.buttonGroup.addButton(self.toolButton)
        
        self.toolButton_2.scene_object_type = RobotItem.item_type()
        self.buttonGroup.addButton(self.toolButton_2)
        
        self.toolButton_3.scene_object_type = ShitItem.item_type()
        self.buttonGroup.addButton(self.toolButton_3)
        
        self.toolButton_4.scene_object_type = ""
        self.buttonGroup.addButton(self.toolButton_4)
        
        self.toolButton_5.scene_object_type = ""
        self.buttonGroup.addButton(self.toolButton_5)
       
        self.buttonGroup.buttonClicked.connect(self.buttonGroupClicked)
        self.graphicsView.drop_new_object.connect(self.drop_new_object)
        
        self.states_group = QtGui.QActionGroup(self)
        self.states_group.addAction(self.action_select_state)
        self.states_group.addAction(self.action_drag_scene)
        self.states_group.triggered.connect(self.on_state_changed)

        self.listView_objects.addAction(self.action_remove)
    
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
            if desc["type"] == BrickItem.item_type():
                self.items_model.add_item(BrickItem(context_menu = self.menu_elements, rect=QtCore.QRectF(-20, -20, 40, 40), name=u"Стена"), pos=desc["scene_pos"])
            elif desc["type"] == RobotItem.item_type():
                self.items_model.add_item(RobotItem(context_menu = self.menu_elements, rect=QtCore.QRectF(-20, -20, 40, 40), name=u"Бендер"), pos=desc["scene_pos"])
            elif desc["type"] == ShitItem.item_type():
                self.items_model.add_item(ShitItem(context_menu = self.menu_elements, rect=QtCore.QRectF(-10, -10, 20, 20), name=u"Хоу-ноу"), pos=desc["scene_pos"])
                
    @pyqtSlot('const QItemSelection &', 'const QItemSelection &')
    def on_listView_objects_selectionChanged(self, selected, deselected):
        self.scene.blockSignals(True)

        self.scene.clearSelection()

        for index in self.listView_objects.selectionModel().selectedIndexes():
            obj = index.data(QtCore.Qt.UserRole).toPyObject()
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

        self.listView_objects.setCurrentIndex(self.items_model.get_index(items[0]))

    @pyqtSlot('bool')
    def on_action_remove_triggered(self, checked):
        for item in self.scene.selectedItems():
            self.items_model.remove_item(item)
    
    @pyqtSlot('bool')
    def on_action_save_triggered(self, checked):
        file_path =  QtGui.QFileDialog.getSaveFileName(self, u"Сохранить сцену", "", "*.json")
        if len(file_path):
            with open(file_path, "wb") as f:
                f.write(json.dumps([item.serialize() for item in self.scene.items()]))

    @pyqtSlot('bool')
    def on_action_load_triggered(self, checked):
        file_path =  QtGui.QFileDialog.getOpenFileName(self, u"Загрузить файл модели", "", "*.json")
        
        if len(file_path):
            self.items_model.clear_items()

            with open(file_path, "rb") as f:
                for desc in json.loads(f.read()):
                    self.items_model.add_item(BaseItem.create(desc), QtCore.QPointF(desc["pos"][0], desc["pos"][1]))

            
        

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
