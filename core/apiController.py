# -*- coding: utf-8 -*-
import sys, os, settings, csv, re
from core import managedb, commandController, apiController, codeGenerator, storage
from pathlib import Path

class ApiControl:

    def __init__(self, cgen=None, entity=None, name=None, keyColumn=None):
        self.entity = entity
        self.name = name
        self.keyColumn = keyColumn
        self.cgen = codeGenerator.CodeGenerator()
        return

    def setEntity(self, entity):
        self.entity = entity + settings.PROTHEUS_ENVIORMENT['default']['COMPANY'] + "0"
        self.cgen.setEntity(entity)
        return

    def setShortName(self, shortName):
        
        self.shortName = shortName.capitalize() if shortName.strip() != "" else shortName[:4]
        self.cgen.setShortName(shortName)
        return

    def setName(self, name):
        
        self.name = name.capitalize()
        if settings.PROTHEUS_ENVIORMENT['default']['DICTIONARY_IN_DATABASE']:
            mdb = managedb.ManagementDb()
            tableList = mdb.getTable(self.entity)
            if len(tableList) > 0 and tableList[0][0].strip() != '':
                self.name = tableList[0][0].strip().capitalize()
                self.name = re.sub('[^A-Za-z0-9 ]+', '', self.name)
                self.name = self.name.replace("  "," ")

        self.cgen.setName(name)
        return

    def setKeyColumn(self, keyColumn):
        self.keyColumn = keyColumn
        return

    #Criate project folders 
    def startProject(self):
        
        if not os.path.isdir(settings.PATH_TEMP): os.mkdir(settings.PATH_TEMP)
        if not os.path.isdir(settings.PATH_FILESTORAGE): os.mkdir(settings.PATH_FILESTORAGE)
        if not os.path.isdir(settings.PATH_SRC): os.mkdir(settings.PATH_SRC)
        if not os.path.isdir(settings.PATH_SRC_DAO): os.mkdir(settings.PATH_SRC_DAO)
        if not os.path.isdir(settings.PATH_SRC_ENTITY): os.mkdir(settings.PATH_SRC_ENTITY)
        if not os.path.isdir(settings.PATH_SRC_LIB): os.mkdir(settings.PATH_SRC_LIB)
        if not os.path.isdir(settings.PATH_SRC_COLLECTION): os.mkdir(settings.PATH_SRC_COLLECTION)
        if not os.path.isdir(settings.PATH_SRC_DOC): os.mkdir(settings.PATH_SRC_DOC)
        if not os.path.isdir(settings.PATH_SRC_API): os.mkdir(settings.PATH_SRC_API)
        if not os.path.isdir(settings.PATH_SRC_MAPPER): os.mkdir(settings.PATH_SRC_MAPPER)
        if not os.path.isdir(settings.PATH_SRC_REQUEST): os.mkdir(settings.PATH_SRC_REQUEST)
        if not os.path.isdir(settings.PATH_SRC_COMMAND): os.mkdir(settings.PATH_SRC_COMMAND)
        if not os.path.isdir(settings.PATH_SRC_VALIDATE): os.mkdir(settings.PATH_SRC_VALIDATE)
        if not os.path.isdir(settings.PATH_SRC_TEST): os.mkdir(settings.PATH_SRC_TEST)
        if not os.path.isdir(settings.PATH_SRC_TEST_CASES): os.mkdir(settings.PATH_SRC_TEST_CASES)
        if not os.path.isdir(settings.PATH_SRC_TEST_GROUP): os.mkdir(settings.PATH_SRC_TEST_GROUP)
        if not os.path.isdir(settings.PATH_SRC_TEST_SUITE): os.mkdir(settings.PATH_SRC_TEST_SUITE)
        
        self.cgen.copyLibs()

        return 

    def addEntity(self):
        stg = storage.Storage()

        if self.entityExist():
            print('Entity '+ self.entity + ' already added! Execute the command #advplapi.py listapi to show the entities added ')
            return
        
        if self.nameExist():
            print('Alias '+ self.name + ' already added! Execute command #advplapi.py listapi to check api added.')
            return

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE,  "storage.entity")

        dataStorage = self.entity+';'+ self.name +';'+self.keyColumn+';'+self.shortName+'\n'
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
                self.setEntity(entity)
                self.setKeyColumn(keyColumn)
                self.setName(name)
                self.setShortName(shortName)
                self.addEntity()

        return

    #List Entity
    def list(self):

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  "storage.entity")
        exists = os.path.isfile(storagePathFile)

        if exists:
            with open(storagePathFile) as datafile:
                data = csv.reader(datafile, delimiter=';')
                print("Your Api's Add")
                for row in data:
                    print('Entity ' + row[0] + ' - Alias Name '+ row[1])
        else:
            print("Not found api, add newapp!")
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

    def build(self):

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  "storage.entity")
        exists = os.path.isfile(storagePathFile) 

        if exists:
            with open(storagePathFile) as datafile:
                data = csv.reader(datafile, delimiter=';')
                for row in data:
                    self.setEntity(row[0])
                    self.setName(row[1])
                    self.setShortName(row[3])
                    self.cgen.buildEntity()
                    self.cgen.buildDao()
                    self.cgen.buildCollection()
                    self.cgen.buildTest()
                    self.cgen.buildMapper()
                    self.cgen.buildRequest()
                    self.cgen.buildCommand()
                    self.cgen.buildValidate()
                    self.cgen.buildDocApiSchema()
                    self.cgen.buildDocApi()
                    self.cgen.buildApi()
                self.cgen.finishApi()
        return False

    def setColumnAlias(self, entity, columnName, aliasName):
                      
        path = os.path.join(settings.PATH_FILESTORAGE , entity + ".columns")
        my_file = Path(path)
        if my_file.is_file():
            exists = False
            file = csv.reader(open(path), delimiter=';')
            lines = list(file)
            tempFile = ""
            
            for row in lines:
                if row[0] == columnName:
                    exists = True
                    row[1] = aliasName
                tempFile += row[0]+";"+row[1]+";"+row[2]+";\n"
            
            if exists:
                f = open(path, "w+")
                f.write(tempFile)
                f.close()
            else:
                print("Column "+ columnName + " not found in "+ entity +"." )    
        else:
            print("Entity "+ entity + " not found, execute command #advplcodegen.py list to list entity.")
            return
        return