# -*- coding: cp1252 -*-
import sys, os, csv, shutil
from advplcodegen import settings
from advplcodegen.core.codeGenerators.codeGenerator import codeGenerator
from string import Template

class AppComponentTsGenerator(codeGenerator):

    def __init__ (self, entity=None, name=None, alias=None, shortName=None):
        super().__init__(entity=None, name=None, alias=None, shortName=None)
        self.templateFile = 'app.component.ts.template' 
        self.templatePath = settings.PATH_TEMPLATE_PO
        self.srcPath = settings.PATH_PO_SRC_APP
        return

    def setFileOut(self):
        self.fileOut = "app.component.ts"
    
    def getVariables(self,storagePathFile):
        menuName = ''
        menus = ''
        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  "storage.entity")
        with open(storagePathFile) as datafile:
            columnInfos = csv.reader(datafile, delimiter=';')
            for columnInfo in columnInfos:
                menuName = columnInfo[4] if len(columnInfo[4]) > 0 else 'Home'
                menus += "    { label: '"+ menuName + "', action: this.onClick.bind(this) },\n"

        variables = { 
                    'menus': menus,
                }
        return variables
