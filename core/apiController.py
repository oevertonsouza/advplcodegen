# -*- encoding: utf-8 -*-
import sys, os, settings, csv
from core import managedb, commandController, apiController, codeGenerator, storage
from pathlib import Path

class ApiControl:

    def __init__(
                self
            ):
        return

    #inicia um projeto criando o diretorio e sub-diretórios
    def startProject(self):
        
        os.mkdir(settings.PATH_API)
        os.mkdir(settings.PATH_API_DAO)
        os.mkdir(settings.PATH_API_ENTITY)
        os.mkdir(settings.PATH_API_LIB)
        os.mkdir(settings.PATH_API_COLLECTION)
        os.mkdir(settings.PATH_API_DOC)

        return 

    #Adiciona um entidade
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

    #Lista as Entidades cadastradas
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

    #Verifica se uma coluna está se repetindo
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


    #Verifica se um alias está se repetindo
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

    #Efetua o build dos codigos -- Cria os codigos com base nas configurações
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


        cgen.copyLibs()
        
        return False



    #Gera as colunas no arquivo .storage, para usar no build
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