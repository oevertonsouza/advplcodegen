# -*- coding: utf-8 -*-
import sys, os, csv, shutil
import settings
from core import managedb, storage
from pathlib import Path
from string import Template

class project:
    prefix  = settings.PROTHEUS_ENVIORMENT['default']['PREFIX']

    def __init__(self):
        return

    #Create project folders 
    def startProject(self):
        self.createDir()

    def createDir(self):
    
        if not os.path.isdir(settings.PATH_TEMP): os.mkdir(settings.PATH_TEMP)
        if not os.path.isdir(settings.PATH_FILESTORAGE): os.mkdir(settings.PATH_FILESTORAGE)
        if not os.path.isdir(settings.PATH_SRC): os.mkdir(settings.PATH_SRC)
        if not os.path.isdir(settings.PATH_SRC_DAO): os.mkdir(settings.PATH_SRC_DAO)
        if not os.path.isdir(settings.PATH_SRC_ENTITY): os.mkdir(settings.PATH_SRC_ENTITY)
        if not os.path.isdir(settings.PATH_SRC_LIB): os.mkdir(settings.PATH_SRC_LIB)
        if not os.path.isdir(settings.PATH_SRC_COLLECTION): os.mkdir(settings.PATH_SRC_COLLECTION)
        if not os.path.isdir(settings.PATH_SRC_DOC): os.mkdir(settings.PATH_SRC_DOC)
        if not os.path.isdir(settings.PATH_SRC_DOC_API): os.mkdir(settings.PATH_SRC_DOC_API)
        if not os.path.isdir(settings.PATH_SRC_DOC_SCHEMA): os.mkdir(settings.PATH_SRC_DOC_SCHEMA)
        if not os.path.isdir(settings.PATH_SRC_API): os.mkdir(settings.PATH_SRC_API)
        if not os.path.isdir(settings.PATH_SRC_MAPPER): os.mkdir(settings.PATH_SRC_MAPPER)
        if not os.path.isdir(settings.PATH_SRC_REQUEST): os.mkdir(settings.PATH_SRC_REQUEST)
        if not os.path.isdir(settings.PATH_SRC_COMMAND): os.mkdir(settings.PATH_SRC_COMMAND)
        if not os.path.isdir(settings.PATH_SRC_VALIDATE): os.mkdir(settings.PATH_SRC_VALIDATE)
        if not os.path.isdir(settings.PATH_SRC_TEST): os.mkdir(settings.PATH_SRC_TEST)
        if not os.path.isdir(settings.PATH_SRC_TEST_CASES): os.mkdir(settings.PATH_SRC_TEST_CASES)
        if not os.path.isdir(settings.PATH_SRC_TEST_GROUP): os.mkdir(settings.PATH_SRC_TEST_GROUP)
        if not os.path.isdir(settings.PATH_SRC_TEST_SUITE): os.mkdir(settings.PATH_SRC_TEST_SUITE)
        
        self.copyLibs()

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
