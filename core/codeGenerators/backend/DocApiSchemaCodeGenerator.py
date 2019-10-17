# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template
from core.daos.model import Entity, Colunas

class DocApiSchemaCodeGenerator(codeGenerator):

    def __init__ (self, entity=None):
        super().__init__(entity=None)
        self.templateFile = 'docApiSchema.template' 
        self.templatePath = settings.PATH_TEMPLATE_DOCS
        self.srcPath = settings.PATH_SRC_DOC_SCHEMA
        return

    def setFileOut(self):
        self.fileOut = self.entity.name.title().replace(" ","")+"_1_100.json"
    
    def getVariables(self):
        properties = ''

        for column in Colunas.select().join(Entity).where(Entity.table == self.entity.table):
            canUpdate = "false" if column.is_indice else "true"
            required = "true" if column.is_keyPathParam else "false"
            
            properties += ''.rjust(16)+(
                '"'+column.name+'": {\n'
                '                    "description": "'+column.desc+'",\n'
                '                    "type": "string",\n'
                '                    "x-totvs": [\n'
                '		                {\n'
                '                           "product": "'+ self.product +'",\n'
                '                           "field": "'+ self.alias +'.'+column.dbField+'",\n'
                '                           "required": '+required+',\n'
                '                           "type": "'+column.dataType+'",\n'
                '                           "length": "'+str(column.length)+'",\n'
                '                           "note": "'+column.desc+'",\n'
                '                           "available": true,\n'
                '                           "canUpdate": '+canUpdate+'\n'                            
                '                        }\n'
                '                   ]\n'
                '                },\n'
                )

            classNameTitle = self.entity.name.title().replace(" ","")
            descriptionPath = self.entity.name.title().replace(" ","")
            descriptionPath = descriptionPath[0].lower() + descriptionPath[1:]
            variables = { 
                    'className': self.entity.name, 
                    'classNameTitle': classNameTitle, 
                    'descriptionPath': descriptionPath, 
                    'entityName' : self.entity.name,
                    'product' : self.product,
                    'productDescription' : self.productDescription,
                    'contact' : self.contact,
                    'segment' : self.segment,
                    'properties' : properties[:-2],
                    'classNameLower' : self.entity.name.lower(),
                }
        return variables
