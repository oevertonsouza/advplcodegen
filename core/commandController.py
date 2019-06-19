# -*- coding: utf-8 -*-
import sys, os, settings
from core import managedb, apiController

class ComandsController:
    
    def __init__(self, firstComands=None, runOk=None, api=None):
        self.firstComands = ['startproject','addcolumn','testconnect', 'addentity', 'list', 'build', 'setcolumnalias']
        self.runOk = False
        self.api = apiController.ApiControl()
        return

    def run(self, run):
        run[1] = run[1].upper()
        script = run[0] if len(run) > 0 else ''
        command = run[1] if len(run) > 1 else ''
        for comand in self.firstComands:
            if command == 'TESTCONNECT':
                mdb = managedb.ManagementDb()
                mdb.testeConnect()
                return
            if command == 'STARTPROJECT':
                self.api.startProject()
                return
            if command == 'ADDENTITY':
                entity = run[2] if len(run) > 2 else ''
                keyColumn = run[3] if len(run) > 3 else ''
                shortName = run[4] if len(run) > 4 else ''
                name = run[5] if len(run) > 5 else ''
                namePortuguese = run[6] if len(run) > 6 else ''
                self.api.setEntity(entity)
                self.api.setKeyColumn(keyColumn)
                self.api.setShortName(shortName)
                self.api.setName(name)
                self.api.setNamePortuguese(namePortuguese)
                self.api.addEntity()
                return
            if command == 'ADDENTITIES':
                file = run[2] if len(run) > 2 else ''
                storagePathFile = os.path.join(os.path.split(file)[0] , os.path.split(file)[1])
                if os.path.isfile(storagePathFile):
                    self.api.addEntities(storagePathFile)
                else:
                    print("can't find or open file " + file)
                return
            if command == 'LIST':
                self.api.list()
                return
            if command == 'BUILD':
                self.api.createDir()
                self.api.build()
                return
            if command == 'SETCOLUMNALIAS':
                entity = run[2] if len(run) > 2 else ''
                columnName = run[3] if len(run) > 3 else ''
                aliasName = run[4] if len(run) > 4 else ''
                self.api.setColumnAlias(entity, columnName, aliasName)
                return
            if command == 'TESTEFUN':
                print("TESTE")
                return
        return

        
