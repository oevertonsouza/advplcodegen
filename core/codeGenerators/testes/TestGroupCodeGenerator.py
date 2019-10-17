# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template
from core.daos.model import Entity, Colunas

class TestGroupCodeGenerator(codeGenerator):

    def __init__ (self, entity=None):
        super().__init__(entity=None)
        self.templateFile = 'TestGroup.template' 
        self.srcPath = settings.PATH_SRC_TEST_GROUP
        return

    def setFileOut(self):
        self.fileOut = self.prefix+self.entity.shortName + "TestGroup.prw"
