# -*- coding: cp1252 -*-
import sys, os, settings, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template

class DefaultModuleTsGenerator(codeGenerator):

    def __init__ (self, entity=None, name=None, alias=None, shortName=None):
        super().__init__(entity=None, name=None, alias=None, shortName=None)
        self.templateFile = 'default.module.ts.template'
        self.templatePath = settings.PATH_TEMPLATE_PO
        self.srcPath = settings.PATH_PO_SRC_APP
        return

    def setFileOut(self):
        self.fileOut = ""
    
    def getVariables(self,entity):
        sufixFileName = '-dynamic-form.module.ts'
        componentName = self.namePortuguese.title().replace(" ","")
        componentNameLower = componentName.lower()
        
        self.fileOut = componentName.lower() + sufixFileName
        self.srcPath = os.path.join(settings.PATH_PO_SRC_APP,self.namePortuguese.replace(" ","").lower())
        
        variables = {
                'componentName': componentName, 
                'componentNameLower' : componentNameLower
            }
        return variables

