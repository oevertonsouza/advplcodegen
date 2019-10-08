# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template

class TestSuiteCodeGenerator(codeGenerator):

    def __init__ (self, entity=None, name=None, alias=None, shortName=None):
        super().__init__(entity=None, name=None, alias=None, shortName=None)
        self.templateFile = 'TestSuite.template' 
        self.srcPath = settings.PATH_SRC_TEST_SUITE
        return

    def setFileOut(self):
        self.fileOut = self.prefix+self.shortName + "TestSuite.prw"
    
    def getVariables(self,entity):
        variables = { 
                'className': entity.shortName, 
                'entity' : entity.name,
                'company' : self.company,
                'filial' : self.filial,
                'prefix' : self.prefix,
            }
        return variables
