# -*- encoding: utf-8 -*-
import sys, os, settings
from core import managedb, apiController

class ComandsController:
    
    def __init__(self, firstComands=None, runOk=None):
        self.firstComands = ['startproject','addcolumn','testconnect', 'newapi']
        self.runOk = False
        return

    def run(self, run):
        for comand in self.firstComands:
            if run[1] == 'testconnect':
                mdb = managedb.ManagementDb()
                mdb.testeConnect()
                return
            if run[1] == 'startproject':
                api = apiController.ApiControl()
                api.startProject()
                return
            if run[1] == 'newapi':
                api = apiController.ApiControl()
                api.newApi(run[2], run[3])
                return
        return 

        
