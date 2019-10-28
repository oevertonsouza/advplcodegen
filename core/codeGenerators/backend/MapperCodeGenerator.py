# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template
from core.daos.model import Entity, Colunas,Relations

class MapperCodeGenerator(codeGenerator):

    def __init__ (self, entity=None):
        super().__init__(entity=None)
        self.templateFile = 'Mapper.template' 
        self.srcPath = settings.PATH_SRC_MAPPER
        return

    def setFileOut(self):
        self.fileOut = self.prefix+"Mpr"+ self.entity.shortName + ".prw"
    
    def getVariables(self):
        mapper = ''
        expandables = []
        expandable = ''
        
        for column in Colunas.select().join(Entity).where(Entity.table == self.entity.table):
            mapper += '    aAdd(self:aFields,{"'+ column.dbField +'" ,"'+ column.name +'"})\n'

        for relation in Relations.select().where(Relations.table == self.entity.table):
            for entity in Entity.select().where(Entity.table == relation.tableRelation):
                expandables.append('"'+entity.name.strip()[:1].lower() + entity.name.strip()[1:] +'"')
        
        if len(expandables) > 0:
            expandable = '    aAdd(self:aExpand,{' + ','.join(expandables) + '})\n'
       
        variables = { 
                'className': self.entity.shortName, 
                'entityName' : self.entity.name,
                'mapper' : mapper,
                'expandable' : expandable,
                'prefix' : self.prefix,
            }
        return variables
