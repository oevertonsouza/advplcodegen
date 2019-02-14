# -*- encoding: utf-8 -*-
import sys, os, settings
from core import managedb, apiController

class ComandsController:
    
    def __init__(self, firstComands=None, runOk=None):
        self.firstComands = ['startproject','addcolumn','testconnect', 'addentity', 'list', 'build']
        self.runOk = False
        return

    def run(self, run):
        api = apiController.ApiControl()
        for comand in self.firstComands:
            if run[1] == 'testconnect':
                mdb = managedb.ManagementDb()
                mdb.testeConnect()
                return
            if run[1] == 'startproject':
                api.startProject()
                return
            if run[1] == 'addentity':
                api.addEntity(run[2], run[3])
                return
            if run[1] == 'list':
                api.list()
                return       
            if run[1] == 'build':
                api.build()
        return 

        
