# -*- coding: cp1252 -*-
import sys, os, settings, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template

class DefaultComponentHtmlGenerator(codeGenerator):

    def __init__ (self, entity=None):
        super().__init__(entity=None)
        self.templateFile = 'default.component.html.template'
        self.templatePath = settings.PATH_TEMPLATE_PO
        self.srcPath = settings.PATH_PO_SRC_APP
        return

    def setFileOut(self):
        self.fileOut = ""
    
    def getVariables(self):
        
        sufixFileName = '-dynamic-form.component.html'
        componentName = self.namePortuguese.replace(" ","").lower()
        apiName = self.namePortuguese
        className = self.namePortuguese.title().replace(" ","")
        jsonName = className[0].lower() + className[1:]
        self.fileOut = componentName + sufixFileName
        self.srcPath = os.path.join(settings.PATH_PO_SRC_APP,self.namePortuguese.replace(" ","").lower())
      
        variables = {
                'apiName' : apiName,
                'jsonName' : jsonName,
            }
        return variables
