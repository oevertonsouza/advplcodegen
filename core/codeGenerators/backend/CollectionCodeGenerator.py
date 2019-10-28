# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from string import Template
from core.codeGenerators.codeGenerator import codeGenerator
from core.daos.model import Entity, Colunas, FromTo, Relations

class CollectionCodeGenerator(codeGenerator):

    def __init__ (self, entity=None):
        super().__init__(entity=None)
        self.templateFile = 'Collection.template'
        self.srcPath = settings.PATH_SRC_COLLECTION
        return

    def setFileOut(self):
        self.fileOut = self.prefix+"Clt"+ self.entity.shortName + ".prw"

    def getVariables(self):
        relations = ''
        column = ''
        columnRelation = ''
        fromtoRelation = []

        for relation in Relations.select().where(Relations.table == self.entity.table):
            for entity in Entity.select().where(Entity.table == relation.tableRelation):
                relations += '    oRelation:setCollection(CenClt' + entity.shortName +'():New())\n'
                relations += '    oRelation:setName("'+ entity.name[:1].lower() + entity.name[1:].strip() +'")\n'
                relations += '    oRelation:setRelationType(' + relation.relationType + ')\n'
                relations += '    oRelation:setBehavior('+ relation.behavior +')\n'
                
                
                for fromto in FromTo.select().where(FromTo.relation_id == relation.id):
                    column = Colunas.select().where(Colunas.dbField == fromto.column)
                    columnRelation = Colunas.select().where(Colunas.dbField == fromto.columnRelation)
                    fromtoRelation.append('    {"'+column[0].name+'","'+columnRelation[0].name+'"}')

                if len(fromtoRelation) > 0:
                    relations += '    oRelation:setFromTo({;\n'
                    relations += '    '+',;\n    '.join(fromtoRelation)  +';\n'
                    relations += '    })\n'
                    relations += '    self:setRelation(oRelation)\n'
        
        variables = { 
            'relations': relations,
            'prefix' : self.prefix,
            'className' : self.entity.shortName
        }

        return variables
