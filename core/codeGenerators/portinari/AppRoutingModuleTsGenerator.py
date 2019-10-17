# -*- coding: cp1252 -*-
import sys, os, settings, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template
from core.daos.model import Entity, Colunas

class AppRoutingModuleTsGenerator(codeGenerator):

    def __init__ (self, entity=None):
        super().__init__(entity=None)
        self.templateFile = 'app-routing.module.ts.template' 
        self.templatePath = settings.PATH_TEMPLATE_PO
        self.srcPath = settings.PATH_PO_SRC_APP
        return

    def setFileOut(self):
        self.fileOut = "app-routing.module.ts"
    
    def getVariables(self):
        routeName = ''
        componentName = ''
        imports = '' 
        routes = ''
        for entity in Entity.select():
            menuName = entity.namePortuguese if entity.namePortuguese != '' else 'Home'
            componentName = entity.namePortuguese.title().replace(" ","")
            componentCammelLower = componentName[:1].lower() + componentName[1:]
            routeName = componentName.lower() 
            routes += ''.rjust(4)+"{ path: '" + routeName + "', loadChildren: './" + routeName + "/" + routeName + ".module#" + componentCammelLower + "Module' },\n"
            routes += ''.rjust(4)+"{ path: '', redirectTo: '/" + routeName + "', pathMatch: 'full'},\n"

        variables = { 
                    'routes': routes,
                }
        return variables
