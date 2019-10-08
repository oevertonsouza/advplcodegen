# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from string import Template
from core.codeGenerators.codeGenerator import codeGenerator
from core.daos.model import Entity, Column

class CommandCodeGenerator(codeGenerator):

    def __init__ (self, entity=None):
        super().__init__(entity=None)
        self.templateFile = 'Command.template' 
        self.srcPath = settings.PATH_SRC_COMMAND
        return

    def setFileOut(self):
        self.fileOut = self.prefix+"Cmd"+ self.entity.shortName +".prw"
