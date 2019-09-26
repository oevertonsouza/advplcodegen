# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template

class RequestCodeGenerator(codeGenerator):

    def __init__ (self, entity=None, name=None, alias=None, shortName=None):
        super().__init__(entity=None, name=None, alias=None, shortName=None)
        self.templateFile = 'Request.template' 
        self.srcPath = settings.PATH_SRC_REQUEST
        return

    def setFileOut(self):
        self.fileOut = self.prefix+"Req"+ self.shortName +".prw"
    
    def getVariables(self,storagePathFile):
        applyFilterAll = ''
        applyFilterSingle = ''
        prepFilter = ''
        with open(storagePathFile) as datafile:
            columnInfo = csv.reader(datafile, delimiter=';')
            for column in columnInfo:
                applyFilterAll += ''.rjust(12)+'self:oCollection:setValue("'+ column[1] +'",self:oRest:'+ column[1] +')\n'
                
                if column[4] == "1" :
                    applyFilterSingle += ''.rjust(12)+'self:oCollection:setValue("'+ column[1] +'",self:oRest:'+ column[1] +')\n'
                    prepFilter += ''.rjust(4)+'self:oCollection:setValue("'+ column[1] +'", self:oRest:'+ column[1] +')\n'

        variables = {
                'className': self.shortName,                     
                'entity' : self.entity,
                'prefix' : self.prefix,
                'applyFilterAll' : applyFilterAll,
                'applyFilterSingle' : applyFilterSingle,
                'prepFilter' : prepFilter,
            }
        return variables
