# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template
from core.daos.model import Entity, Colunas

class RequestCodeGenerator(codeGenerator):

    def __init__ (self, entity=None):
        super().__init__(entity=None)
        self.templateFile = 'Request.template' 
        self.srcPath = settings.PATH_SRC_REQUEST
        return

    def setFileOut(self):
        self.fileOut = self.prefix+"Req"+ self.entity.shortName +".prw"
    
    def getVariables(self):
        applyFilterAll = ''
        applyFilterSingle = ''
        prepFilter = ''
        
        for column in Colunas.select().join(Entity).where(Entity.table == self.entity.table):
            applyFilterAll += ''.rjust(12)+'self:oCollection:setValue("'+ column.name +'",self:oRest:'+ column.name +')\n'
            
            if column.is_indice :
                applyFilterSingle += ''.rjust(12)+'self:oCollection:setValue("'+ column.name +'",self:oRest:'+ column.name +')\n'
                prepFilter += ''.rjust(4)+'self:oCollection:setValue("'+ column.name +'", self:oRest:'+ column.name +')\n'

        variables = {
                'className': self.entity.shortName,                     
                'entityName' : self.entity.name,
                'prefix' : self.prefix,
                'applyFilterAll' : applyFilterAll,
                'applyFilterSingle' : applyFilterSingle,
                'prepFilter' : prepFilter,
            }
        return variables
