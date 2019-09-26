# -*- coding: cp1252 -*-
import sys, os, settings, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template

class DefaultComponentTsGenerator(codeGenerator):

    def __init__ (self, entity=None, name=None, alias=None, shortName=None):
        super().__init__(entity=None, name=None, alias=None, shortName=None)
        self.templateFile = 'default.component.ts.template'
        self.templatePath = settings.PATH_TEMPLATE_PO
        self.srcPath = settings.PATH_PO_SRC_APP
        return

    def setFileOut(self):
        self.fileOut = ""
    
    def getVariables(self,storagePathFile):
        sufixFileName = '-dynamic-form.component.ts'
        componentName = self.namePortuguese.replace(" ","").lower()
        className = self.namePortuguese.title().replace(" ","")
        jsonName = className[0].lower() + className[1:]
        self.fileOut = componentName + sufixFileName
        self.srcPath = os.path.join(settings.PATH_PO_SRC_APP,self.namePortuguese.replace(" ","").lower())
        
        variables = {
                'componentName' : componentName,
                'jsonName' : jsonName,
                'className' : className
            }
        return variables
