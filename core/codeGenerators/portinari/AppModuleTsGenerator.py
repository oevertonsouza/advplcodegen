# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template
from core.daos.model import Entity, Column

class AppModuleTsGenerator(codeGenerator):

    def __init__ (self, entity=None):
        super().__init__(entity=None)
        self.templateFile = 'app.module.ts.template' 
        self.templatePath = settings.PATH_TEMPLATE_PO
        self.srcPath = settings.PATH_PO_SRC_APP
        return

    def setFileOut(self):
        self.fileOut = "app.module.ts"
    
    def getVariables(self):

        declarations = []
        routeName = ''
        componentName =''
        imports = '' 

        for entity in Entity.select():
            componentName = entity.namePortuguese if entity.namePortuguese != '' else 'Home'
            routeName = componentName.lower() 
            declarations.append('    '+componentName + 'Component')
            if componentName != 'Home':
                imports += "import { "+ componentName + 'Component'" } from './"+ routeName +"/"+ routeName +"-dynamic-form.component';\n"

        variables = { 
                    'imports': imports,
                    'declarations' : ',\n'.join(declarations)
                }
        return variables

