# -*- coding: cp1252 -*-
import csv
import os
import shutil
import sys
from string import Template
from core.daos.model import Entity, Colunas

import settings
from core.codeGenerators.codeGenerator import codeGenerator


class ApiCodeGenerator(codeGenerator):

    def __init__ (self, entity=None):
        super().__init__(entity=None)
        self.templateFile = 'Entity.template' 
        self.srcPath = settings.PATH_SRC_API
        return

    def setFileOut(self):
        self.fileOut = self.prefix+"Rest"+ self.segment +".prw"
    
    def getVariables(self):
        wsDataKeys = ''
        wsDataNoKeys = ''
        defaultVarsNoKey = ''
        defaultVarsKey = ''
        varskey = []
        varsNokey = []
        keyVarsNoKeyPath = []
        keyPath = ''

        for column in Colunas.select().join(Entity).where(Entity.table == self.entity.table):

            if not column.name in self.columnsToAdd:
                self.columnsToAdd.append(column.name)
                wsDataNoKeys += ''.rjust(4)+'WSDATA '+ column.name +' as STRING  OPTIONAL\n'

            if column.is_indice :
                defaultVarsKey  += ''.rjust(4)+'Default self:'+ column.name +' := ""\n'
                varskey.append(''.rjust(4)+column.name)
                keyVarsNoKeyPath.append(''.rjust(4)+column.name)
            else:
                defaultVarsNoKey  += ''.rjust(4)+'Default self:'+ column.name +' := ""\n'
                varsNokey.append(''.rjust(4)+column.name)
            
            if column.is_keyPathParam :
                keyPath = column.name
        if len(keyVarsNoKeyPath) > 0:
            keyVarsNoKeyPath.remove('    '+keyPath)
            descriptionPath = self.entity.name.title().replace(" ","").replace("-","").strip()
            descriptionPath = descriptionPath[0].lower() + descriptionPath[1:]
            variables = {
                    'classNameAbreviate': self.entity.shortName,
                    'description': self.entity.name.title(),
                    'descriptionPath': descriptionPath,
                    'className': self.entity.shortName,
                    'classNameLower' : self.entity.shortName.lower(),
                    'table' : self.entity.table,
                    'entityName' : self.entity.name,
                    'prefix' : self.prefix,
                    'segment' : self.segment,
                    'wsDataKeys' : wsDataKeys,
                    'wsDataNoKeys' : wsDataNoKeys,
                    'defaultVarsKey' : defaultVarsKey,
                    'defaultVarsNoKey' : defaultVarsNoKey,
                    'varskey' : ',;\n'.join(varskey)+ ',;' if len(varsNokey) > 0 else ',;\n'.join(varskey)+ ';' ,
                    'varsNokey' : ',;\n'.join(varsNokey)+';',
                    'keyPath' : keyPath,
                    'keyVarsNoKeyPath' : ',;\n'.join(keyVarsNoKeyPath)+';',
                }

        return variables

    def build(self):
        variables = self.getVariables()
        self.makeTempFile(variables,'Api.Header',"")
        self.makeTempFile(variables,'Api.Header.WsData',self.entity.table)
        self.makeTempFile(variables,'Api.Header.Methods',self.entity.table)
        #footer
        self.makeTempFile(variables,'Api.Body',self.entity.table)
        return

    def makeTempFile(self, variables, file, table):
        fileIn = open(os.path.join(settings.PATH_TEMPLATE, file+'.template'))
        temp = Template(fileIn.read())
        result = temp.substitute(variables)
        f = open(os.path.join(settings.PATH_TEMP, file + table + ".tmp") , "w+")
        f.write(result)
        f.close()
    
    def finishApi(self):
        self.setFileOut()
        header = open(os.path.join(settings.PATH_TEMP, 'Api.Header.tmp')).read()
        footer = open(os.path.join(settings.PATH_TEMPLATE, 'Api.Footer.template')).read()
        wsData = ''
        methods = ''
        body = ''
        for files in os.walk(settings.PATH_TEMP):
            for file in files[2]:
                storagePathFile = os.path.join(settings.PATH_TEMP,file )
                exists = os.path.isfile(storagePathFile) 
                if exists:
                    with open(storagePathFile) as datafile:
                        if 'Api.Header.Methods' in file:
                            methods += datafile.read()
                        elif 'Api.Header.WsData' in file:
                            wsData += datafile.read()
                        elif 'Api.Body' in file:
                            body += datafile.read()
        result = header+wsData+methods+footer+body

        f = open(os.path.join(self.srcPath, self.fileOut) , "w+")
        f.write(result)
        f.close()
        return
