#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtCore import pyqtSlot, pyqtSignal
import json

class DragToolButton(QtGui.QToolButton):
    def __init__(self, parent=None):
        super(QtGui.QWidget, self).__init__(parent)
    
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.dragStartPosition = event.pos()

        super(DragToolButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        super(DragToolButton, self).mouseMoveEvent(event)
        
        if not (event.buttons() & QtCore.Qt.LeftButton):
            return

        if (event.pos() - self.dragStartPosition).manhattanLength() < QtGui.QApplication.startDragDistance():
            return

        drag = QtGui.QDrag(self)
        mimeData = QtCore.QMimeData()
        mimeData.setData("application/scene-item-type", json.dumps({"type": self.scene_object_type}))
        drag.setMimeData(mimeData)
        drag.setPixmap(self.icon().pixmap(self.size()))
        drag.setHotSpot(QtCore.QPoint(self.width() / 2, self.height() / 2))
        dropAction = drag.exec_()

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    widget = DragLabel()
    widget.show()
    app.exec_()
