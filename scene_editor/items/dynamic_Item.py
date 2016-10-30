#!/usr/bin/python
# -*- coding: utf-8 -*-
from PyQt4 import QtCore
from scene_editor.items.base_item import BaseItem
import scene_editor.resourses


class DynamicItem(BaseItem):
    update_timer = QtCore.QTimer()

    def __init__(self, image=None, **kw_args):
        super(DynamicItem, self).__init__(**kw_args)
        self.set_editable(False)
        self.set_attach_grid(False)
        self._image = image

        if self._image is not None:
            self._source = QtCore.QRectF(
                0.0, 0.0, self._image.width(), self._image.height())

        if not self.update_timer.isActive():
            self.update_timer.start(1000 / 33)

        self.update_timer.timeout.connect(self.update_state)

    def paint_item(self, painter, option, widget):
        if self._image is not None:
            painter.drawImage(self.get_rect(), self._image, self._source)

    def update_state(self):
        '''Производит какойто процесс'''
        pass
