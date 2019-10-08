# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template
from core.daos.model import Entity, Column

class ValidateCodeGenerator(codeGenerator):

    def __init__ (self, entity=None):
        super().__init__(entity=None)
        self.templateFile = 'Validator.template' 
        self.srcPath = settings.PATH_SRC_VALIDATE
        return

    def setFileOut(self):
        self.fileOut = self.prefix+"Vld"+ self.entity.shortName +".prw"
