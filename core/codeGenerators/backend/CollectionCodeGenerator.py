# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from string import Template
from core.codeGenerators.codeGenerator import codeGenerator

class CollectionCodeGenerator(codeGenerator):

    def __init__ (self, entity=None, name=None, alias=None, shortName=None):
        super().__init__(entity=None, name=None, alias=None, shortName=None)
        self.templateFile = 'Collection.template'
        self.srcPath = settings.PATH_SRC_COLLECTION
        return

    def setFileOut(self):
        self.fileOut = self.prefix+"Clt"+ self.shortName + ".prw"
    
    def getVariables(self,entity):
        variables = { 
                'className': entity.shortName, 
                'entity' : entity.name,
                'prefix' : self.prefix,
                }

        return variables
