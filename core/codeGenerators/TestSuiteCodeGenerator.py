# -*- coding: cp1252 -*-
import sys, os, csv, shutil
from advplcodegen import settings
from codeGenerator import codeGenerator
from string import Template

class TestSuiteCodeGenerator(codeGenerator):

    def __init__ (self, entity=None, name=None, alias=None, shortName=None):
        super().__init__(entity=None, name=None, alias=None, shortName=None)
        self.templateFile = 'TestSuite.template' 
        self.srcPath = settings.PATH_SRC_TEST_SUITE
        return

    def setFileOut(self):
        self.fileOut = self.prefix+self.shortName + "TestSuite.prw"
    
    def getVariables(self,storagePathFile):
        variables = { 
                'className': self.shortName, 
                'entity' : self.entity,
                'company' : self.company,
                'filial' : self.filial,
                'prefix' : self.prefix,
            }
        return variables
