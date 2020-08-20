# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from string import Template
from core.codeGenerators.codeGenerator import codeGenerator
from core.daos.model import Entity, Colunas, RelationKeys, Relations

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
        relationKey = []
        relationName = ''
        count = Relations.select().where(Relations.table == self.entity.table).count()
        index = 1


        for relation in Relations.select().where(Relations.table == self.entity.table):
            for entity in Entity.select().where(Entity.table == relation.tableRelation):
                relations += '    oRelation:setCollection(CenClt' + entity.shortName +'():New())\n'
                relationName = entity.name.title().replace(" ","").replace("-","").strip()
                relationName = relationName[0].lower() + relationName[1:]
                relations += '    oRelation:setName("'+ relationName +'")\n'
                relations += '    oRelation:setRelationType(' + relation.relationType + ')\n'
                relations += '    oRelation:setBehavior('+ relation.behavior +')\n'
                
            for relationKey in RelationKeys.select().where(RelationKeys.relation_id == relation.id):
                column = Colunas.select().where(Colunas.dbField == relationKey.column)
                columnRelation = Colunas.select().where(Colunas.dbField == relationKey.columnRelation)
                relationKey.append('    {"'+column[0].name+'","'+columnRelation[0].name+'"}')

            if len(relationKey) > 0:
                relations += '    oRelation:setRelationKey({;\n'
                relations += '    '+',;\n    '.join(relationKey)  +';\n'
                relations += '    })\n'
                relations += '    self:setRelation(oRelation)\n\n'
            
            relationKey =[] #limpa o array from to 
            
            if index < count:
                relations += '    oRelation := CenRelation():New()\n\n' #quando h� mais de uma rela��o 'expandable'

            index = index + 1

        variables = { 
            'relations': relations,
            'prefix' : self.prefix,
            'className' : self.entity.shortName
        }

        return variables
