# -*- coding: utf-8 -*-
import sys, os, settings, csv, re
from core import managedb, storage
from pathlib import Path

class entityController:

    def __init__(self, entity=None, name=None, keyColumn=None, namePortuguese=None):
        self.entity = entity
        self.name = name
        self.namePortuguese = namePortuguese
        self.keyColumn = keyColumn
        return

    def setEntity(self, entity):
        self.entity = entity + settings.PROTHEUS_ENVIORMENT['default']['COMPANY'] + "0"
        return

    def setShortName(self, shortName):
        
        self.shortName = shortName.title() if shortName.strip() != "" else shortName[:4]
        return

    def setName(self, name):
        
        self.name = name.title()
        if settings.PROTHEUS_ENVIORMENT['default']['DICTIONARY_IN_DATABASE']:
            mdb = managedb.ManagementDb()
            tableList = mdb.getTable(self.entity)
            if len(tableList) > 0 and tableList[0][0].strip() != '':
                self.name = tableList[0][0].strip().title()
                self.name = re.sub('[^A-Za-z0-9 ]+', '', self.name)
                self.name = self.name.replace("  "," ")

        return

    def setNamePortuguese(self, namePortuguese):
        
        self.namePortuguese = namePortuguese.title()
        if settings.PROTHEUS_ENVIORMENT['default']['DICTIONARY_IN_DATABASE']:
            mdb = managedb.ManagementDb()
            tableList = mdb.getTable(self.entity)
            if len(tableList) > 0 and tableList[0][1].strip() != '':
                self.namePortuguese = tableList[0][1].strip().title()
                self.namePortuguese = re.sub('[^A-Za-z0-9 ]+', '', self.namePortuguese)
                self.namePortuguese = self.namePortuguese.replace("  "," ")

        return

    def setKeyColumn(self, keyColumn):
        self.keyColumn = keyColumn
        return

    def addEntity(self):
        stg = storage.Storage()

        if self.entityExist():
            print('Entity '+ self.entity + ' already added! Execute the command #advplcodegen.py list to show the entities added ')
            return
        
        if self.nameExist():
            print('Alias '+ self.name + ' already added! Execute command #advplcodegen.py list to check api added.')
            return

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE,  "storage.entity")

        dataStorage = self.entity+';'+ self.name +';'+self.keyColumn+';'+self.shortName+';'+self.namePortuguese+'\n'
        exists = os.path.isfile(storagePathFile) 

        if exists:
            with open(storagePathFile, 'a') as file:
                file.write(dataStorage)
                file.close()
        else:
            f = open(storagePathFile , "w+")
            f.write(dataStorage)
            f.close()

        stg.genColumnStorage(self.entity, self.keyColumn)
        print('Entity '+ self.entity + ' successfully added!')

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
                self.setEntity(entity)
                self.setKeyColumn(keyColumn)
                self.setName(name)
                self.setShortName(shortName)
                self.setNamePortuguese(namePortuguese)
                self.addEntity()

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

    def entityExist(self):

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  "storage.entity")
        exists = os.path.isfile(storagePathFile) 

        if exists:
            with open(storagePathFile) as datafile:
                data = csv.reader(datafile, delimiter=';')
                for row in data:
                    if len(row) > 0 and row[0] == self.entity:
                        return True
        else:
            return False
        return False

    def nameExist(self):

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  "storage.entity")
        exists = os.path.isfile(storagePathFile) 

        if exists:
            with open(storagePathFile) as datafile:
                data = csv.reader(datafile, delimiter=';')
                for row in data:
                    if len(row) > 0:
                        return row[1] == self.name
        else:
            return False
        return False