# -*- coding: cp1252 -*-
import sys, os, settings, csv, shutil
from advplcodegen import settings
from advplcodegen.core.codeGenerators.codeGenerator import codeGenerator
from string import Template

class AppRoutingModuleTsGenerator(codeGenerator):

    def __init__ (self, entity=None, name=None, alias=None, shortName=None):
        super().__init__(entity=None, name=None, alias=None, shortName=None)
        self.templateFile = 'app-routing.module.ts.template' 
        self.templatePath = settings.PATH_TEMPLATE_PO
        self.srcPath = settings.PATH_PO_SRC_APP
        return

    def setFileOut(self):
        self.fileOut = "app-routing.module.ts"
    
    def getVariables(self,storagePathFile):
        routeName = ''
        componentName = ''
        imports = '' 
        routes = ''
        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  "storage.entity")
        with open(storagePathFile) as datafile:
            columnInfos = csv.reader(datafile, delimiter=';')
            for columnInfo in columnInfos:
                componentName = columnInfo[4].replace(" ","") if len(columnInfo[4]) > 0 else 'Home'
                routeName = componentName.lower() 
                routes += ''.rjust(4)+"{ path: '" + routeName + "' , component: " +  componentName + 'Component' " },\n"
                if componentName != 'Home':
                    imports += "import { "+ componentName + 'Component'" } from './"+ routeName +"/"+ routeName +".component';\n"

        variables = { 
                    'imports': imports,
                    'routes': routes,
                }
        return variables
