# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template

class EnvironmentTsGenerator(codeGenerator):

    def __init__ (self, entity=None):
        super().__init__(entity=None)
        self.templateFile = 'environment.ts.template' 
        self.templatePath = settings.PATH_TEMPLATE_PO_ENVIRONMENTS
        self.srcPath = settings.PATH_PO_SRC_ENVIRONMENTS
        return

    def setFileOut(self):
        self.fileOut = "environment.ts"
    
    def getVariables(self):
        variables = { 
                    'segment': self.segment,
                }
        return variables
