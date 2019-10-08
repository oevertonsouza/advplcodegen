# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template

class AppComponentTsGenerator(codeGenerator):

    def __init__ (self, entity=None):
        super().__init__(entity=None)
        self.templateFile = 'app.component.ts.template' 
        self.templatePath = settings.PATH_TEMPLATE_PO
        self.srcPath = settings.PATH_PO_SRC_APP
        return

    def setFileOut(self):
        self.fileOut = "app.component.ts"
    
    def getVariables(self):
        linkName = ""
        menuName = ''
        menus = ''
        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  "storage.entity")
        with open(storagePathFile) as datafile:
            columnInfos = csv.reader(datafile, delimiter=';')
            for columnInfo in columnInfos:
                menuName = columnInfo[4] if len(columnInfo[4]) > 0 else 'Home'
                linkName = menuName.replace(" ","").lower()
                menus += "    { label: '"+ menuName + "', link: '"+ linkName +"'},\n"

        variables = { 
                    'menus': menus,
                }
        return variables
