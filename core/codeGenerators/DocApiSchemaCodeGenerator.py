# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template

class DocApiSchemaCodeGenerator(codeGenerator):

    def __init__ (self, entity=None, name=None, alias=None, shortName=None):
        super().__init__(entity=None, name=None, alias=None, shortName=None)
        self.templateFile = 'docApiSchema.template' 
        self.templatePath = settings.PATH_TEMPLATE_DOCS
        self.srcPath = settings.PATH_SRC_DOC_SCHEMA
        return

    def setFileOut(self):
        self.fileOut = self.name.title().replace(" ","")+"_1_100.json"
    
    def getVariables(self, storagePathFile):
        properties = ''

        with open(storagePathFile) as datafile:
            columnInfo = csv.reader(datafile, delimiter=';')
            for column in columnInfo:
                canUpdate = "false" if column[4] == "1" else "true"
                required = "true" if column[5] == "1" else "false"
                
                properties += ''.rjust(16)+(
                    '"'+column[1]+'": {\n'
                    '                    "description": "'+column[6]+'",\n'
                    '                    "type": "string",\n'
                    '                    "x-totvs": [\n'
                    '		                {\n'
                    '                           "product": "'+ self.product +'",\n'
                    '                           "field": "'+ self.alias +'.'+column[0]+'",\n'
                    '                           "required": '+required+',\n'
                    '                           "type": "'+column[2]+'",\n'
                    '                           "length": "'+column[3]+'",\n'
                    '                           "note": "'+column[6]+'",\n'
                    '                           "available": true,\n'
                    '                           "canUpdate": '+canUpdate+'\n'                            
                    '                        }\n'
                    '                   ]\n'
                    '                },\n'
                    )

            classNameTitle = self.name.title().replace(" ","")
            descriptionPath = self.name.title().replace(" ","")
            descriptionPath = descriptionPath[0].lower() + descriptionPath[1:]
            variables = { 
                    'className': self.name, 
                    'classNameTitle': classNameTitle, 
                    'descriptionPath': descriptionPath, 
                    'entity' : self.entity,
                    'product' : self.product,
                    'productDescription' : self.productDescription,
                    'contact' : self.contact,
                    'segment' : self.segment,
                    'properties' : properties[:-2],
                    'classNameLower' : self.name.lower(),
                }
        return variables
