# -*- coding: utf-8 -*-
import sys, os, csv, shutil
import settings
from core import managedb, storage
from pathlib import Path
from string import Template
from core.daos import model
from core.daos.model import Entity, Colunas

class poProject:
    prefix  = settings.PROTHEUS_ENVIORMENT['default']['PREFIX']

    def __init__(self):
        self.poSrcPath = settings.PATH_PO_SRC_APP
        self.storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  "storage.entity")
        return

    def startPoProject(self):
        model.CreateTables()
        self.createDir()

    def createDir(self):
        pathDir = ''
        dirName = ''                                    
        
        for entity in Entity.select():
            dirName = entity.namePortuguese.replace(" ","").lower() if len(entity.namePortuguese) > 0 else 'home'
            pathDir = os.path.join(self.poSrcPath, dirName)
            if dirName != 'home':
                if not os.path.isdir(pathDir): os.mkdir(pathDir)
                if not os.path.isdir(pathDir+"\\"+dirName+"-view"): os.mkdir(pathDir+"\\"+dirName+"-view")
                if not os.path.isdir(pathDir+"\\"+dirName+"-form"): os.mkdir(pathDir+"\\"+dirName+"-form")
                if not os.path.isdir(pathDir+"\\"+dirName+"-list"): os.mkdir(pathDir+"\\"+dirName+"-list")
        self.copyLibs()
        return

    def copyLibs(self):
        
        shutil.copy(settings.PATH_TEMPLATE_PO + '\\app.component.css', settings.PATH_PO_SRC_APP + '\\app.component.css')
        shutil.copy(settings.PATH_TEMPLATE_PO + '\\app.component.html', settings.PATH_PO_SRC_APP + '\\app.component.html')
        shutil.copy(settings.PATH_TEMPLATE_PO + '\\app.component.spec.ts', settings.PATH_PO_SRC_APP + '\\app.component.spec.ts')
        shutil.copy(settings.PATH_TEMPLATE_PO + '\\app.module.ts', settings.PATH_PO_SRC_APP + '\\app.module.ts')
        pathDir = os.path.join(settings.PATH_PO_SRC_APP, 'shared')
        if not os.path.isdir(pathDir): os.mkdir(pathDir)
        return
