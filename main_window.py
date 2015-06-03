#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal
from items.base_item import BaseItem
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
    GAS_STATION_ID = 5
    
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
        self.buttonGroup.addButton(self.toolButton, self.BORDER_ID)
        self.buttonGroup.addButton(self.toolButton_2, self.ROBOT_ID)
        self.buttonGroup.addButton(self.toolButton_3, self.SHIT_ID)
        self.buttonGroup.addButton(self.toolButton_4, self.STORAGE_ID)
        self.buttonGroup.addButton(self.toolButton_5, self.GARAGE_ID)
        self.buttonGroup.addButton(self.toolButton_6, self.GAS_STATION_ID)
        
        self.scene.left_button_clicked.connect(self.on_left_button_clicked)
        self.buttonGroup.buttonClicked[int].connect(self.buttonGroupClicked)
    
    def buttonGroupClicked(self, id):
        buttons = self.buttonGroup.buttons()
        for button in buttons:
            if self.buttonGroup.button(id) != button:
                button.setChecked(False)
    
    def on_left_button_clicked(self, event):
        object_id = self.buttonGroup.checkedId()

        if object_id != -1:
            self.buttonGroup.checkedButton().setChecked(False)
            self.scene.clearSelection()

            if object_id == self.BORDER_ID:
                #создание обьектов
                item = BaseItem(self.menu_elements)
                item.setData(0, {"name": u"Стена"})
                self.scene.addItem(item)
                item.setPos(event.scenePos())
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
