# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template
from core.daos.model import Entity, Colunas

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
        menuList = ''
        
        for entity in Entity.select():
            menuName = entity.namePortuguese if entity.namePortuguese != '' else 'Home'
            linkName = menuName.replace(" ","").lower()
            menuList += "    { label: '"+ menuName + "', link: '"+ linkName +"'},\n"

        variables = { 
                    'menuList': menuList,
                }
        return variables
