# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template

class ValidateCodeGenerator(codeGenerator):

    def __init__ (self, entity=None, name=None, alias=None, shortName=None):
        super().__init__(entity=None, name=None, alias=None, shortName=None)
        self.templateFile = 'Validator.template' 
        self.srcPath = settings.PATH_SRC_VALIDATE
        return

    def setFileOut(self):
        self.fileOut = self.prefix+"Vld"+ self.shortName +".prw"
    
    def getVariables(self, storagePathFile):
        variables = {
                'className': self.shortName,
                'entity' : self.entity,                    
                'prefix' : self.prefix,
            }
        return variables
