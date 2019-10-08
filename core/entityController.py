# -*- coding: utf-8 -*-
import sys, os, csv, re
import settings
from core import managedb, storage
from pathlib import Path
from core.daos.model import Entity, Column
from core.entities import aliasEntity
import peewee

class entityController:

    def __init__(self, entity=None, name=None, keyColumn=None, namePortuguese=None):
        self.entity = entity
        self.name = name
        self.namePortuguese = namePortuguese
        self.keyColumn = keyColumn
        return

    def addEntity(self, entity):
        mdb = managedb.ManagementDb()
        tableInfo = mdb.getTableInfo(entity.table)
        if len(tableInfo) > 0:
            entity.name = tableInfo[0][0]
            entity.namePortuguese = tableInfo[0][1]
        new_entity = self.saveEntity(entity)
        self.saveColumns(new_entity)
        return

    def saveEntity(self, entity):
        try:
            new_entity = Entity.create(name = entity.name,
                    table = entity.tableName,
                    shortName = self.entity.shortName,
                    namePortuguese = entity.namePortuguese,
                    keyColumn = entity.keyColumn)
            operationMessage = 'added'
        except peewee.IntegrityError:
            new_entity = Entity.get(table = entity.tableName)
            new_entity.name = entity.name
            new_entity.table = entity.tableName
            new_entity.shortName = self.entity.shortName
            new_entity.namePortuguese = entity.namePortuguese
            new_entity.keyColumn = entity.keyColumn
            new_entity.save()
            operationMessage = 'updated'
        print('Entity '+ entity.tableName + ' successfully ' + operationMessage + '!')
        return new_entity

    def saveColumns(self, entity):
        mdb = managedb.ManagementDb()
        tableInfo = mdb.getTableInfo(entity.table)
        uniqueColumns = tableInfo[0][2].strip().split('+')
        columnList = mdb.getColumnDesc(entity.table)
       
        for field in columnList:
            is_indice = field[0] in uniqueColumns
            is_keyPathParam = field[0] == entity.keyColumn 
            name = re.sub('[^A-Za-z0-9]+', '', field[2].title())
            name = name[0].lower() + name[1:]
            desc = field[7].strip()
            opcoes = field[6].strip().replace(";",",")
            length = str(field[4])
            if field[3] == 'C':
                dataType = "string"
            elif field[3] == 'D':
                dataType = "date"
            elif field[3] == 'N':
                dataType = "float"
                length = str(int(field[4]))
            else:  
                dataType = "string"
            varName = field[3].lower() + re.sub('[^A-Za-z0-9]+', '', field[1].title())
            try:
                new_column = Column.create( entity = entity,
                            dbField = field[0],
                            name = name,
                            dataType = dataType,
                            length = length,
                            is_indice = is_indice,
                            is_required = False,
                            is_keyPathParam = is_keyPathParam,
                            desc = desc,
                            variabelName = varName,
                            options = opcoes)
            except peewee.IntegrityError:
                new_column = Column.get(Column.dbField == field[0])
                new_column.entity = entity
                new_column.dbField = field[0]
                new_column.name = name
                new_column.dataType = dataType
                new_column.length = length
                new_column.is_indice = is_indice
                new_column.is_keyPathParam = is_keyPathParam
                new_column.is_required = is_indice
                new_column.desc = desc
                new_column.variabelName = varName
                new_column.options = opcoes
                new_column.save()
        if len(columnList) > 0:
            print('Entity '+ entity.table + ', columns saved!')
        else:
            print('Entity '+ entity.table + ' without columns in database!')
        return

    def addEntities(self,file):
        
        with open(file) as datafile:
            columnInfo = csv.reader(datafile, delimiter=';')
            for column in columnInfo:
                entity = column[0] if len(column) > 0 else ''
                keyColumn = column[1] if len(column) > 1 else ''
                shortName = column[2] if len(column) > 2 else ''
                name = column[3] if len(column) > 3 else ''
                namePortuguese = column[4] if len(column) > 4 else ''
                entity = aliasEntity.AliasEntity(entity, name, keyColumn, namePortuguese, shortName)
                self.addEntity(entity)

        return

    #List Entity
    def list(self):
        
        for entity in Entity.select():
            print('Entity ' + entity.table + ' - Alias Name '+ entity.name)
        return
