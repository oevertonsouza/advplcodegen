# -*- coding: cp1252 -*-
import sys, os, settings, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template

class DefaultComponentTsGenerator(codeGenerator):

    def __init__ (self, entity=None):
        super().__init__(entity=None)
        self.templateFile = 'default.component.ts.template'
        self.templatePath = settings.PATH_TEMPLATE_PO
        self.srcPath = settings.PATH_PO_SRC_APP
        return

    def setFileOut(self):
        self.fileOut = ""
    
    def getVariables(self):
        fieldsDetails = ''
        sufixFileName = '-dynamic-form.component.ts'
        componentName = self.namePortuguese.replace(" ","").lower()
        className = self.namePortuguese.title().replace(" ","")
        jsonName = className[0].lower() + className[1:]
        self.fileOut = componentName + sufixFileName
        self.srcPath = os.path.join(settings.PATH_PO_SRC_APP,self.namePortuguese.replace(" ","").lower())

        with open(storagePathFile) as datafile:
            columnInfos = csv.reader(datafile, delimiter=';')
            for columnInfo in columnInfos:
                fieldsDetails += "    { property: '"+ columnInfo[6] +"', divider: '', required: true, minLength: 4, maxLength: 50, gridColumns: 6, gridSmColumns: 12 },\n"
        
        variables = {
                'componentName' : componentName,
                'jsonName' : jsonName,
                'className' : className,
                'fieldsDetails' : fieldsDetails
            }
        return variables
