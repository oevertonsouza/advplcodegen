# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template

class DocApiCodeGenerator(codeGenerator):

    def __init__ (self, entity=None, name=None, alias=None, shortName=None):
        super().__init__(entity=None, name=None, alias=None, shortName=None)
        self.templateFile = 'docApi.template' 
        self.templatePath = settings.PATH_TEMPLATE_DOCS
        self.srcPath = settings.PATH_SRC_DOC_API
        return

    def setFileOut(self):
        self.fileOut = self.name.title().replace(" ","")+"_v1_100.json"
    
    def getVariables(self, storagePathFile):
        pathParam = ''
        queryParam = ''
        parameters = ''
        keyParameters = ''
        keyPath = ''
        abreviate = self.shortName

        with open(storagePathFile) as datafile:
            columnInfo = csv.reader(datafile, delimiter=';')
            for column in columnInfo:
                parameters += '                    {\n'
                parameters += '                        "$ref": "#/components/parameters/'+column[1]+'Param"\n'
                parameters += '                    },\n'    
                
                if column[4] == "1" :
                    keyParameters += '                    {\n'
                    keyParameters += '                        "$ref": "#/components/parameters/'+column[1]+'Param"\n'
                    keyParameters += '                    },\n'

                if column[5] == "1":
                    keyPath = column[1]
                    pathParam = (
                                    '           "'+column[1]+'Param": {\n'
                                    '               "name": "'+column[1]+'",\n'
                                    '               "in": "path",\n'
                                    '               "description": "'+column[6]+'",\n'
                                    '               "required": true,\n'
                                    '               "schema": {\n'
                                    '		            "type": "string",\n'
                                    '	                "format": "string"\n'
                                    '               }\n'
                                    '           },\n'
                    )
                else :
                    if column[4] == "1":
                        queryParam += (
                                        '           "'+column[1]+'Param": {\n'
                                        '               "name": "'+column[1]+'",\n'
                                        '               "in": "query",\n'
                                        '               "description": "'+column[6]+'",\n'
                                        '               "required": true,\n'
                                        '               "schema": {\n'
                                        '		            "type": "string",\n'
                                        '	                "format": "string"\n'
                                        '               }\n'
                                        '           },\n'
                        )
                    else: 
                        queryParam += (
                                        '           "'+column[1]+'Param": {\n'
                                        '               "name": "'+column[1]+'",\n'
                                        '               "in": "query",\n'
                                        '               "description": "'+column[6]+'",\n'
                                        '               "required": false,\n'
                                        '               "schema": {\n'
                                        '		            "type": "string",\n'
                                        '	                "format": "string"\n'
                                        '               }\n'
                                        '           },\n'
                        )

            classNameTitle = self.name.title().replace(" ","")
            descriptionPath = classNameTitle[0].lower() + classNameTitle[1:]
            variables = { 
                    'className': self.name,
                    'classNamePortuguese': self.namePortuguese,
                    'classNameTitle': classNameTitle,
                    'descriptionPath': descriptionPath,
                    'entity' : self.entity,
                    'product' : self.product,
                    'productDescription' : self.productDescription,
                    'contact' : self.contact,
                    'segment' : self.segment,
                    'pathParam' : pathParam,
                    'parameters' : parameters[:-2],
                    'queryParam' : queryParam[:-3]+"}",
                    'classNameLower' : self.name.lower(),
                    'keyParameters' : keyParameters[:-2],
                    'keyPath' : keyPath,
                    'abreviate' : abreviate,
                }

        return variables
