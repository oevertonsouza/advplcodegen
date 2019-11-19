# -*- coding: utf-8 -*-
import sys, re
import settings
from pathlib import Path

class AliasEntity:

    def __init__(self, table=None, name=None, keyColumn=None, namePortuguese=None, shortName=None, columns=None):
        self.table = table
        self.setTableName(table)
        self.setName(name)
        self.setShortName(shortName)
        self.setNamePortuguese(namePortuguese)
        self.setKeyColumn(keyColumn)
        self.columns = columns
        return

    def setTableName(self, table):
        self.tableName = table + settings.PROTHEUS_ENVIORMENT['default']['COMPANY'] + "0"
        return

    def setShortName(self, shortName):
        self.shortName = shortName.title() if shortName.strip() != "" else shortName[:4]
        return

    def setName(self, name):
        self.name = name.replace("-"," ").replace("."," ")
        self.name = self.name.strip().title()
        self.name = re.sub('[^A-Za-z0-9 ]+', '', self.name)
        self.name = self.name.replace("  "," ")
        return

    def setNamePortuguese(self, namePortuguese):
        self.namePortuguese = namePortuguese.replace("-"," ").replace("."," ")
        self.namePortuguese = self.namePortuguese.strip().title()
        self.namePortuguese = re.sub('[^A-Za-z0-9 ]+', '', self.namePortuguese)
        self.namePortuguese = self.namePortuguese.replace("  "," ")
        return

    def setKeyColumn(self, keyColumn):
        self.keyColumn = keyColumn
        return
