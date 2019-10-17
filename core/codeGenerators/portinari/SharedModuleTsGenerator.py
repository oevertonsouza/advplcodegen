# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template

class SharedModuleTsGenerator(codeGenerator):

    def __init__ (self, entity=None):
        super().__init__(entity=None)
        self.templateFile = 'shared.module.ts.template' 
        self.templatePath = settings.PATH_TEMPLATE_PO_SHARED
        self.srcPath = settings.PATH_PO_SRC_APP_SHARED
        return

    def setFileOut(self):
        self.fileOut = "shared.module.ts"
    
    def getVariables(self):
        variables = { 
                    'segment': self.segment,
                }
        return variables
