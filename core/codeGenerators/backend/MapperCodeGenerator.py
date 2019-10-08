# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template

class MapperCodeGenerator(codeGenerator):

    def __init__ (self, entity=None, name=None, alias=None, shortName=None):
        super().__init__(entity=None, name=None, alias=None, shortName=None)
        self.templateFile = 'Mapper.template' 
        self.srcPath = settings.PATH_SRC_MAPPER
        return

    def setFileOut(self):
        self.fileOut = self.prefix+"Mpr"+ self.shortName + ".prw"
    
    def getVariables(self,entity):
        mapper = ''
        
        with open(storagePathFile) as datafile:
            columnInfo = csv.reader(datafile, delimiter=';')
            for column in columnInfo:
                mapper += '    aAdd(self:aFields,{"'+ column[0] +'" ,"'+ column[1] +'"})\n'
            
            variables = { 
                    'className': entity.shortName, 
                    'entity' : entity.name,
                    'mapper' : mapper,
                    'prefix' : self.prefix,
                }
        return variables
