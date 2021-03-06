#!/usr/bin/python
# -*- coding: utf-8 -*-
import math
import time
from PyQt4 import QtGui
from scene_editor.items.dynamic_Item import DynamicItem
import scene_editor.resourses


class ModelInterface:
    def __init__(self, model_id):
        self.model_id = model_id

    def send_cmd(self, cmd, params=None):
        if self.model_id == 0:
            if cmd == "get_angle":
                return math.cos(time.time())


class RobotItem(DynamicItem):
    def __init__(self, **kw_args):
        super(RobotItem, self).__init__(
            image=QtGui.QImage(":/images/textures/bulldozer-top.png"),
            **kw_args)
        self.model_interface = ModelInterface(0)

    @staticmethod
    def item_type():
        return "RobotItem"

    @staticmethod
    def deserialize(desc):
        return RobotItem(**desc)

    def update_state(self):
        '''Производит какойто процесс'''
        self.rotate(self.model_interface.send_cmd("get_angle"))


DynamicItem.FACTORY_MAP[RobotItem.item_type()] = RobotItem.deserialize
