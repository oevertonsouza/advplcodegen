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
        stg = storage.Storage()

        if self.entityExist(entity):
            print('Entity '+ entity.tableName + ' already added! Execute the command #.py list to show the entities added ')
            return
        
        if self.nameExist(entity.name):
            print('Alias '+ entity.name + ' already added! Execute command #.py list to check api added.')
            return

        try:
            new_entity = Entity.create(name = entity.name,
                    table = entity.tableName,
                    shortName = entity.shortName,
                    namePortuguese = entity.namePortuguese,
                    keyColumn = entity.keyColumn)
        except peewee.IntegrityError:
            new_entity = Entity.get(table = entity.tableName)
        stg.genColumnStorage(new_entity)
        print('Entity '+ entity.tableName + ' successfully added!')

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

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  "storage.entity")
        exists = os.path.isfile(storagePathFile)

        if exists:
            with open(storagePathFile) as datafile:
                data = csv.reader(datafile, delimiter=';')
                print("Your entities added")
                for row in data:
                    print('Entity ' + row[0] + ' - Alias Name '+ row[1])
        else:
            print("No entities found!")
        return

    def entityExist(self, entity):

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  "storage.entity")
        exists = os.path.isfile(storagePathFile) 

        if exists:
            with open(storagePathFile) as datafile:
                data = csv.reader(datafile, delimiter=';')
                for row in data:
                    if len(row) > 0 and row[0] == entity.tableName:
                        return True
        else:
            return False
        return False

    def nameExist(self,name):

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  "storage.entity")
        exists = os.path.isfile(storagePathFile) 

        if exists:
            with open(storagePathFile) as datafile:
                data = csv.reader(datafile, delimiter=';')
                for row in data:
                    if len(row) > 0:
                        return row[1] == name
        else:
            return False
        return False