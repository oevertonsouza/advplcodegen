# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template
from core.daos.model import Entity, Colunas

class DocApiCodeGenerator(codeGenerator):

    def __init__ (self, entity=None):
        super().__init__(entity=None)
        self.templateFile = 'docApi.template' 
        self.templatePath = settings.PATH_TEMPLATE_DOCS
        self.srcPath = settings.PATH_SRC_DOC_API
        return

    def setFileOut(self):
        self.fileOut = self.entity.name.title().replace(" ","")+"_v1_100.json"
    
    def getVariables(self):
        pathParam = ''
        queryParam = ''
        parameters = ''
        keyParameters = ''
        keyPath = ''
        abreviate = self.entity.shortName
        for column in Colunas.select().join(Entity).where(Entity.table == self.entity.table):
            parameters += '                    {\n'
            parameters += '                        "$ref": "#/components/parameters/'+column.name+'Param"\n'
            parameters += '                    },\n'    
            
            if column.is_indice :
                keyParameters += '                    {\n'
                keyParameters += '                        "$ref": "#/components/parameters/'+column.name+'Param"\n'
                keyParameters += '                    },\n'

            if column.is_keyPathParam:
                keyPath = column.name
                pathParam = (
                            '           "'+column.name+'Param": {\n'
                            '               "name": "'+column.name+'",\n'
                            '               "in": "path",\n'
                            '               "description": "'+column.desc+'",\n'
                            '               "required": true,\n'
                            '               "schema": {\n'
                            '		            "type": "string",\n'
                            '	                "format": "string"\n'
                            '               }\n'
                            '           },\n'
                )
            else:
                    queryParam += (
                                    '           "'+column.name+'Param": {\n'
                                    '               "name": "'+column.name+'",\n'
                                    '               "in": "query",\n'
                                    '               "description": "'+column.desc+'",\n'
                                    '               "required": ' + 'true' if column.is_indice else 'false' +  ',\n'
                                    '               "schema": {\n'
                                    '		            "type": "string",\n'
                                    '	                "format": "string"\n'
                                    '               }\n'
                                    '           },\n'
                    )
            
            classNameTitle = self.entity.name.title().replace(" ","")
            descriptionPath = classNameTitle[0].lower() + classNameTitle[1:]
            variables = { 
                    'className': self.entity.name,
                    'classNamePortuguese': self.entity.namePortuguese,
                    'classNameTitle': classNameTitle,
                    'descriptionPath': descriptionPath,
                    'entityName' : self.entity.name,
                    'product' : self.product,
                    'productDescription' : self.productDescription,
                    'contact' : self.contact,
                    'segment' : self.segment,
                    'pathParam' : pathParam,
                    'parameters' : parameters[:-2],
                    'queryParam' : queryParam[:-3]+"}",
                    'classNameLower' : self.entity.name.lower(),
                    'keyParameters' : keyParameters[:-2],
                    'keyPath' : keyPath,
                    'abreviate' : abreviate,
                }

        return variables
