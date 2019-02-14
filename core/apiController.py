# -*- encoding: utf-8 -*-
import sys, os, settings, csv

from core import managedb, commandController, apiController, codeGenerator

class ApiControl:

    def __init__(
                self
            ):
        return

    def startProject(self):
        
        os.mkdir(settings.PATH_API)
        os.mkdir(settings.PATH_API_DAO)
        os.mkdir(settings.PATH_API_ENTITY)
        os.mkdir(settings.PATH_API_LIB)
        os.mkdir(settings.PATH_API_SEEKER)

        return 

    def addEntity(self, entity, alias):

        if self.entityExist(entity, alias):
            print('Entity '+ entity + ' already added! Execute command #advplapi.py listapi ')
            return
        
        if self.aliasExist(entity, alias):
            print('Alias '+ alias + ' already added! Execute command #advplapi.py listapi to check api added.')
            return

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  "apistorage.entity")
        dataStorage = entity+';'+ alias+'\n'
        exists = os.path.isfile(storagePathFile) 
        


        if exists:
            with open(storagePathFile, 'a') as file:
                file.write(dataStorage)
                file.close()
        else:
            f = open(storagePathFile , "w+")
            f.write(dataStorage)
            f.close()

        self.generateColumnsStorage(entity)

        return

    def list(self):

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  "apistorage.entity")
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

    def entityExist(self, entity, alias):

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  "apistorage.txt")
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


    def aliasExist(self, entity, alias):

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  "apistorage.entity")
        exists = os.path.isfile(storagePathFile) 

        if exists:
            with open(storagePathFile) as datafile:
                data = csv.reader(datafile, delimiter=';')
                for row in data:
                    if row[1] == alias:
                        return True
        else:
            return False
        return False

    def build(self):

        cgen = codeGenerator.CodeGenerator()

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  "apistorage.entity")
        exists = os.path.isfile(storagePathFile) 

        if exists:
            with open(storagePathFile) as datafile:
                data = csv.reader(datafile, delimiter=';')
                for row in data:
                    cgen.builderEntity(row[0], row[1])


        return False

    def generateColumnsStorage(self, entity):
        
        f = open(os.path.join(settings.PATH_FILESTORAGE , entity + ".columns"), "w+")

        mdb = managedb.ManagementDb()
        columnInfo = mdb.getColumnInfo(entity)

        for column in columnInfo:
            f.write(column[0] +';;'+column[1]+'\n')
        
        f.close()

        return    


