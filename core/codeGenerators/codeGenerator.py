# -*- coding: cp1252 -*-
import sys, os, settings, csv, shutil
from advplcodegen import settings
from advplcodegen.core import managedb, commandController, codeGenController
from string import Template



class codeGenerator():

    prefix  = settings.PROTHEUS_ENVIORMENT['default']['PREFIX']
    product = settings.PROTHEUS_ENVIORMENT['default']['PRODUCT']
    productDescription = settings.PROTHEUS_ENVIORMENT['default']['PRDUCT_DESCRIPTION']
    contact = settings.PROTHEUS_ENVIORMENT['default']['CONTACT']
    segment = settings.PROTHEUS_ENVIORMENT['default']['SEGMENT']
    company = settings.PROTHEUS_ENVIORMENT['default']['COMPANY']
    filial = settings.PROTHEUS_ENVIORMENT['default']['FILIAL']
    columnsToAdd = []
    templateFile = '' 
    fileOut = ''
    srcPath = ''

    def __init__ (self, entity=None, name=None, alias=None, shortName=None):
        self.entity = entity,
        self.shortName = shortName,
        self.name = name,
        self.alias = alias,
        self.templatePath = settings.PATH_TEMPLATE
        return

    def setEntity(self, entity):
        self.entity = entity
        self.alias = entity[:3]
        return

    def setShortName(self, shortName):
        self.shortName = shortName
        return

    def setName(self, name):
        self.name = name
        return

    def setNamePortuguese(self, namePortuguese):
        self.namePortuguese = namePortuguese
        return
    
    def writeFile(self, variables):
        fileIn = open(os.path.join(self.templatePath, self.templateFile))   
        temp = Template(fileIn.read())
        result = temp.substitute(variables)

        f = open(os.path.join(self.srcPath, self.fileOut) , "w+")
        f.write(result)
        f.close()
        return
    
    def getVariables(self,storagePathFile):
        return('','')
        
    def setFileOut(self):
        return

    def build(self):
        self.setFileOut()
        storagePathFile = os.path.join(settings.PATH_FILESTORAGE, self.entity + ".columns")
        exists = os.path.isfile(storagePathFile)
        if exists:
            variables = self.getVariables(storagePathFile)
            self.writeFile(variables)
        return
