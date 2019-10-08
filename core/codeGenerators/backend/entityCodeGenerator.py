# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template
from core.daos.model import Entity, Column

class entityCodeGenerator(codeGenerator):

    def __init__ (self, entity=None):
        super().__init__(entity=None)
        self.templateFile = 'Entity.template' 
        self.srcPath = settings.PATH_SRC_ENTITY
        return

    def setFileOut(self):
        self.fileOut = self.prefix+self.entity.shortName + ".prw"
    
    def getVariables(self):
        serialize = ''
        fields    = ''
        for column in Column.select().join(Entity).where(Entity.table == self.entity.table):
            serialize   += '    oJsonControl:setProp(oJson,"' + column.name + '",self:getValue("'+ column.name+'")) /* Column '+ column.dbField +' */ \n'
            fields      += '    self:oFields:push({"'+column.name+'", self:getValue("'+column.name +'")}) /* Column '+ column.dbField +' */ \n'
            
        variables = { 
                'className': self.entity.shortName, 
                'description': self.entity.name, 
                'serialize' : serialize,
                'fields' : fields,
                'table' : self.entity.table,
                'prefix' : self.prefix,
            }
        return variables
