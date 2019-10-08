# -*- coding: cp1252 -*-
import sys, os, settings, csv, shutil
import settings
from core import managedb, commandController, codeGenController
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

    def __init__ (self, entity=None):
        self.entity = entity
        self.templatePath = settings.PATH_TEMPLATE
        return

    def setEntity(self, entity):
        self.entity = entity
        self.alias = entity.table[:3]
        return
    
    def writeFile(self, variables):
        fileIn = open(os.path.join(self.templatePath, self.templateFile))   
        temp = Template(fileIn.read())
        result = temp.substitute(variables)
        f = open(os.path.join(self.srcPath, self.fileOut) , "w+", encoding="utf-8")
        f.write(result)
        f.close()
        return
    
    def getVariables(self):
        variables = {
                'className': self.entity.shortName,                     
                'entity' : self.entity.name,
                'prefix' : self.prefix,
                }
        return variables
        
    def setFileOut(self):
        return

    def build(self):
        self.setFileOut()
        self.writeFile(self.getVariables())
        return
