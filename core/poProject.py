# -*- coding: utf-8 -*-
import sys, os, csv, shutil
import settings
from core import managedb, storage
from pathlib import Path
from string import Template
from core.daos import model
from core.daos.model import Entity, Column

class poProject:
    prefix  = settings.PROTHEUS_ENVIORMENT['default']['PREFIX']

    def __init__(self):
        self.poSrcPath = settings.PATH_PO_SRC_APP
        self.storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  "storage.entity")
        return

    #Create project folders 
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
        return

    def copyLibs(self):
        
        src_files = os.listdir(settings.PATH_TEMPLATE_LIBS)
        for file_name in src_files:
            fileIn = open(os.path.join(settings.PATH_TEMPLATE_LIBS, file_name))
            temp = Template(fileIn.read())
            result = temp.substitute({'prefix': self.prefix})
            fileIn.close()
            file = file_name.split('.')
            f = open(os.path.join(settings.PATH_SRC_LIB, self.prefix+file[0]+'.prw' ) , "w+")
            f.write(result)
            f.close()
        return
