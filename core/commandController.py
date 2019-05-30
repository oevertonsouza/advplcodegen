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
        for comand in self.firstComands:
            if run[1] == 'TESTCONNECT':
                mdb = managedb.ManagementDb()
                mdb.testeConnect()
                return
            if run[1] == 'STARTPROJECT':
                self.api.startProject()
                return
            if run[1] == 'ADDENTITY':
                self.api.setEntity(run[2])
                self.api.setName(run[3])
                self.api.setKeyColumn(run[4])
                self.api.addEntity()
                return
            if run[1] == 'LIST':
                self.api.list()
                return
            if run[1] == 'BUILD':
                self.api.build()
                return
            if run[1] == 'SETCOLUMNALIAS':
                script = run[0]
                command = run[1]
                entity = run[2]
                columnName = run[3]
                aliasName = run[4]
                self.api.setColumnAlias(entity, columnName, aliasName)
                return
            if run[1] == 'TESTEFUN':
                print("TESTE")
                return
        return

        
