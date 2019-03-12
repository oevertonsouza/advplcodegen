# -*- encoding: utf-8 -*-
import sys, os, settings, csv
from core import managedb, commandController, apiController, codeGenerator, storage
from pathlib import Path

class ApiControl:

    def __init__(
                self
            ):
        return

    #Criate project folders 
    def startProject(self):
        
        os.mkdir(settings.PATH_SRC)
        os.mkdir(settings.PATH_SRC_DAO)
        os.mkdir(settings.PATH_SRC_ENTITY)
        os.mkdir(settings.PATH_SRC_LIB)
        os.mkdir(settings.PATH_SRC_COLLECTION)
        os.mkdir(settings.PATH_SRC_DOC)
        os.mkdir(settings.PATH_SRC_API)
        os.mkdir(settings.PATH_SRC_MAPPER)
        os.mkdir(settings.PATH_SRC_RESTREQUEST)
        os.mkdir(settings.PATH_SRC_TEST)
        os.mkdir(settings.PATH_SRC_TEST_CASES)
        os.mkdir(settings.PATH_SRC_TEST_GROUP)
        os.mkdir(settings.PATH_SRC_TEST_SUITE)

        cgen = codeGenerator.CodeGenerator()
        cgen.copyLibs()

        return 

    def addEntity(self, entity, name):

        stg = storage.Storage()

        if self.entityExist(entity, name):
            print('Entity '+ entity + ' already added! Execute command #advplapi.py listapi ')
            return
        
        if self.nameExist(entity, name):
            print('Alias '+ name + ' already added! Execute command #advplapi.py listapi to check api added.')
            return

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  "storage.entity")
        dataStorage = entity+';'+ name +'\n'
        exists = os.path.isfile(storagePathFile) 

        if exists:
            with open(storagePathFile, 'a') as file:
                file.write(dataStorage)
                file.close()
        else:
            f = open(storagePathFile , "w+")
            f.write(dataStorage)
            f.close()

        stg.genColumnStorage(entity)

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

    def entityExist(self, entity, name):

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  "storage.txt")
        exists = os.path.isfile(storagePathFile) 

        if exists:
            with open(storagePathFile) as datafile:
                data = csv.reader(datafile, delimiter=';')
                for row in data:
                    if row[0] == entity:
                        return True
        else:
            return False
        return False

    def nameExist(self, entity, name):

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  "storage.entity")
        exists = os.path.isfile(storagePathFile) 

        if exists:
            with open(storagePathFile) as datafile:
                data = csv.reader(datafile, delimiter=';')
                for row in data:
                    if row[1] == name:
                        return True
        else:
            return False
        return False

    def build(self):

        cgen = codeGenerator.CodeGenerator()
        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  "storage.entity")
        exists = os.path.isfile(storagePathFile) 

        if exists:
            with open(storagePathFile) as datafile:
                data = csv.reader(datafile, delimiter=';')
                for row in data:
                    cgen.buildEntity(row[0], row[1])
                    cgen.buildDao(row[0], row[1])
                    cgen.buildCollection(row[0], row[1])
                    cgen.buildTest(row[0], row[1])
                    cgen.buildMapper(row[0], row[1])
                    cgen.buildRequest(row[0], row[1])
        
        return False

    def setColumnAlias(self, entity, columnName, aliasName):
        
        temp = ''
        existsColuns = False                
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