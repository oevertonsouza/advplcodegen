# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template
from core.daos.model import Entity, Colunas

class TestSuiteCodeGenerator(codeGenerator):

    def __init__ (self, entity=None):
        super().__init__(entity=None)
        self.templateFile = 'TestSuite.template' 
        self.srcPath = settings.PATH_SRC_TEST_SUITE
        return

    def setFileOut(self):
        self.fileOut = self.prefix+self.entity.shortName + "TestSuite.prw"
    
    def getVariables(self):
        variables = { 
                'className': self.entity.shortName, 
                'entityName' : self.entity.name,
                'company' : self.company,
                'filial' : self.filial,
                'prefix' : self.prefix,
            }
        return variables
