# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template
from core.daos.model import Entity, Colunas, Relations

class entityCodeGenerator(codeGenerator):

    def __init__ (self, entity=None):
        super().__init__(entity=None)
        self.templateFile = 'Entity.template' 
        self.srcPath = settings.PATH_SRC_ENTITY
        return

    def setFileOut(self):
        self.fileOut = self.prefix+self.entity.shortName + ".prw"
    
    def getVariables(self):
        expandable = ''
        expandables = []
        serialize  = ''
        fields     = ''
        
        for column in Colunas.select().join(Entity).where(Entity.table == self.entity.table):
            serialize += '    oJsonControl:setProp(oJson,"' + column.name + '",self:getValue("'+ column.dbField.strip()+'")) \n'
            fields    += '    self:oFields:push({"'+column.name+'", self:getValue("'+column.dbField.strip() +'")}) \n'

        for relation in Relations.select().where(Relations.table == self.entity.table):
            for entity in Entity.select().where(Entity.table == relation.tableRelation):
                expandable = entity.name.title().replace(" ","").replace("-","").strip()
                expandable = expandable[0].lower() + expandable[1:]
                expandables.append('"'+ expandable +'"')
        
        if len(expandables) > 0:
            expandable = '    oJson["_expandables"] := {' + ','.join(expandables) + '}\n'
             
        variables = { 
                'className': self.entity.shortName, 
                'description': self.entity.name, 
                'expandable' : expandable,
                'serialize' : serialize,
                'fields' : fields,
                'table' : self.entity.table,
                'prefix' : self.prefix,
            }
        return variables
