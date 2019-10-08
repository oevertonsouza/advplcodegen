# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template
from core.daos.model import Entity, Column

class DaoCodeGenerator(codeGenerator):

    def __init__ (self, entity=None):
        super().__init__(entity=None)
        self.templateFile = 'Dao.template' 
        self.srcPath = settings.PATH_SRC_DAO
        return

    def setFileOut(self):
        self.fileOut = self.prefix+"Dao"+ self.entity.shortName + ".prw"
    
    def getVariables(self):
        commitKey = ''
        commitNoKey = ''
        bscChaPrim = ''
        loadOrder = ''
        cfieldOrder = []

        for column in Column.select().join(Entity).where(Entity.table == self.entity.table):
            loadOrder += ''.rjust(4)+'self:oHashOrder:set("'+ column.dbField +'", "'+ column.name +'")\n'
            if column.is_indice:
                cfieldOrder.append(column.dbField)
                commitKey += ''.rjust(12)+self.alias+'->'+column.dbField+' := _Super:normalizeType('+ self.alias +'->'+ column.dbField +',self:getValue("'+ column.name +'")) /* Column '+ column.dbField +' */\n'
                bscChaPrim += ''.rjust(4)+'cQuery += " AND ' +column.dbField+ ' = ? "\n'
                bscChaPrim += ''.rjust(4)+'aAdd(self:aMapBuilder, self:toString(self:getValue("'+column.name+'")))\n'
            else:
                commitNoKey += ''.rjust(8)+self.alias+'->'+column.dbField+' := _Super:normalizeType('+ self.alias +'->'+ column.dbField +',self:getValue("'+ column.name +'")) /* Column '+ column.dbField +' */\n'
                    
            variables = { 
                    'className': self.entity.shortName,
                    'alias': self.alias,
                    'entity' : self.entity.name,
                    'commitKey' : commitKey,
                    'commitNoKey' : commitNoKey,
                    'loadOrder' : loadOrder,
                    'cfieldOrder' : ','.join(cfieldOrder),
                    'bscChaPrim' : bscChaPrim,
                    'prefix' : self.prefix,
                }
        return variables
