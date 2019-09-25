# -*- coding: utf-8 -*-
import sys, os, settings
from advplcodegen.core import managedb, codeGenController, project, poProject, entityController

class ComandsController:
    
    def __init__(self, firstComands=None, runOk=None, api=None):
        self.firstComands = ['startproject','addcolumn','testconnect', 'addentity', 'list', 'build']
        self.runOk = False
        self.codeGen = codeGenController.codeGenController()
        self.project = project.project()
        self.poProject = poProject.poProject()
        self.entities = entityController.entityController()
        return

    def run(self, run):
        run[1] = run[1].upper()
        command = run[1] if len(run) > 1 else ''

        if command == 'TESTCONNECT':
            mdb = managedb.ManagementDb()
            mdb.testeConnect()
            return
        if command == 'STARTPROJECT':
            self.project.startProject()
            return
        if command == 'ADDENTITY':
            entity = run[2] if len(run) > 2 else ''
            keyColumn = run[3] if len(run) > 3 else ''
            shortName = run[4] if len(run) > 4 else ''
            name = run[5] if len(run) > 5 else ''
            namePortuguese = run[6] if len(run) > 6 else ''
            self.entities.setEntity(entity)
            self.entities.setKeyColumn(keyColumn)
            self.entities.setShortName(shortName)
            self.entities.setName(name)
            self.entities.setNamePortuguese(namePortuguese)
            self.entities.addEntity()
            return
        if command == 'ADDENTITIES':
            file = run[2] if len(run) > 2 else ''
            storagePathFile = os.path.join(os.path.split(file)[0] , os.path.split(file)[1])
            if os.path.isfile(storagePathFile):
                self.entities.addEntities(storagePathFile)
            else:
                print("can't find or open file " + file)
            return
        if command == 'LIST':
            self.entities.list()
            return
        if command == 'BUILD':
            self.project.createDir()
            self.codeGen.build()
            return
        if command == 'PO-BUILD':
            self.poProject.createDir()
            self.codeGen.PoBuild()
        if command == 'TESTEFUN':
            print("TESTE")
            return
        return

        
