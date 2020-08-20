# -*- coding: utf-8 -*-
import sys, re
import settings
from pathlib import Path

class AliasRelation:

    def __init__(self, tableFather=None, tableSon=None, behavior=None, relationType=None, keys=None):
        self.setTableFather(tableFather)
        self.setTableSon(tableSon)
        self.setBehavior(behavior)
        self.setRelationType(relationType)
        self.setKeys(keys)
        return

    def setTableFather(self, tableFather):
        self.tableFather = tableFather
        return

    def setTableSon(self,tableSon):
        self.tableSon = tableSon
        return
    
    def setBehavior(self,behavior):
        self.behavior = behavior
        return
    
    def setRelationType(self,relationType):
        self.relationType = relationType
        return

    def setKeys(self,keys):
        self.keys = keys.split(',')
        return