# -*- coding: cp1252 -*-
import sys, os, settings, csv, shutil
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template

class DaoCodeGenerator(codeGenerator):

    def __init__ (self, entity=None, name=None, alias=None, shortName=None):
        super().__init__(entity=None, name=None, alias=None, shortName=None)
        self.templateFile = 'Dao.template' 
        self.srcPath = settings.PATH_SRC_DAO
        return

    def setFileOut(self):
        self.fileOut = self.prefix+"Dao"+ self.shortName + ".prw"
    
    def getVariables(self,storagePathFile):
        commitKey = ''
        commitNoKey = ''
        bscChaPrim = ''
        loadOrder = ''
        cfieldOrder = []

        with open(storagePathFile) as datafile:
            columnInfo = csv.reader(datafile, delimiter=';')

            for column in columnInfo:
                loadOrder += ''.rjust(4)+'self:oHashOrder:set("'+ column[0] +'", "'+ column[1] +'")\n'
                
                if column[4] == "1" :
                    cfieldOrder.append(column[0])
                    commitKey += ''.rjust(12)+self.alias+'->'+column[0]+' := _Super:normalizeType('+ self.alias +'->'+ column[0] +',self:getValue("'+ column[1] +'")) /* Column '+ column[0] +' */\n'
                    bscChaPrim += ''.rjust(4)+'cQuery += " AND ' +column[0]+ ' = ? "\n'
                    bscChaPrim += ''.rjust(4)+'aAdd(self:aMapBuilder, self:toString(self:getValue("'+column[1]+'")))\n'
                else:
                    commitNoKey += ''.rjust(8)+self.alias+'->'+column[0]+' := _Super:normalizeType('+ self.alias +'->'+ column[0] +',self:getValue("'+ column[1] +'")) /* Column '+ column[0] +' */\n'
                    
            variables = { 
                    'className': self.shortName,
                    'alias': self.alias,
                    'entity' : self.entity,
                    'commitKey' : commitKey,
                    'commitNoKey' : commitNoKey,
                    'loadOrder' : loadOrder,
                    'cfieldOrder' : ','.join(cfieldOrder),
                    'bscChaPrim' : bscChaPrim,
                    'prefix' : self.prefix,
                }
        return variables
