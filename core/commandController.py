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
        print(run)
        for comand in self.firstComands:
            if run[1] == 'testConnect':
                mdb = managedb.ManagementDb()
                mdb.testeConnect()
                return
            if run[1] == 'startProject':
                self.api.startProject()
                return
            if run[1] == 'addEntity':
                print(run[1])
                self.api.setEntity(run[2])
                self.api.setName(run[3])
                self.api.setKeyColumn(run[4])
                self.api.addEntity()
                return
            if run[1] == 'list':
                self.api.list()
                return
            if run[1] == 'build':
                self.api.build()
                return
            if run[1] == 'setColumnAlias':
                script = run[0]
                command = run[1]
                entity = run[2]
                columnName = run[3]
                aliasName = run[4]
                self.api.setColumnAlias(entity, columnName, aliasName)
                return
            if run[1] == 'testefun':
                print("teste")
                return
        return

        
