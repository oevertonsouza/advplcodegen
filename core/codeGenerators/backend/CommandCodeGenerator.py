# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from string import Template
from core.codeGenerators.codeGenerator import codeGenerator

class CommandCodeGenerator(codeGenerator):

    def __init__ (self, entity=None, name=None, alias=None, shortName=None):
        super().__init__(entity=None, name=None, alias=None, shortName=None)
        self.templateFile = 'Command.template' 
        self.srcPath = settings.PATH_SRC_COMMAND
        return

    def setFileOut(self):
        self.fileOut = self.prefix+"Cmd"+ self.shortName +".prw"
    
    def getVariables(self,storagePathFile):
        variables = {
                'className': self.shortName,                     
                'entity' : self.entity,
                'prefix' : self.prefix,
                }
        return variables
