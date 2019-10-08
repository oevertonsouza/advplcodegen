# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template

class AppModuleTsGenerator(codeGenerator):

    def __init__ (self, entity=None, name=None, alias=None, shortName=None):
        super().__init__(entity=None, name=None, alias=None, shortName=None)
        self.templateFile = 'app.module.ts.template' 
        self.templatePath = settings.PATH_TEMPLATE_PO
        self.srcPath = settings.PATH_PO_SRC_APP
        return

    def setFileOut(self):
        self.fileOut = "app.module.ts"
    
    def getVariables(self,entity):

        declarations = []
        routeName = ''
        componentName =''
        imports = '' 
        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  "storage.entity")

        with open(storagePathFile) as datafile:
            columnInfos = csv.reader(datafile, delimiter=';')
            for columnInfo in columnInfos:

                componentName = columnInfo[4].replace(" ","") if len(columnInfo[4]) > 0 else 'Home'
                routeName = componentName.lower() 
                declarations.append('    '+componentName + 'Component')
                if componentName != 'Home':
                    imports += "import { "+ componentName + 'Component'" } from './"+ routeName +"/"+ routeName +"-dynamic-form.component';\n"

        variables = { 
                    'imports': imports,
                    'declarations' : ',\n'.join(declarations)
                }
        return variables

