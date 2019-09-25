# -*- coding: cp1252 -*-
import csv
import os
import shutil
import sys
from string import Template

from advplcodegen import settings
from advplcodegen.core.codeGenerators.codeGenerator import codeGenerator


class ApiCodeGenerator(codeGenerator):

    def __init__ (self, entity=None, name=None, alias=None, shortName=None):
        super().__init__(entity=None, name=None, alias=None, shortName=None)
        self.templateFile = 'Entity.template' 
        self.srcPath = settings.PATH_SRC_API
        return

    def setFileOut(self):
        self.fileOut = self.prefix+"Rest"+ self.segment +".prw"
    
    def getVariables(self,storagePathFile):
        wsDataKeys = ''
        wsDataNoKeys = ''
        defaultVarsNoKey = ''
        defaultVarsKey = ''
        varskey = []
        varsNokey = []
        keyVarsNoKeyPath = []
        keyPath = ''

        with open(storagePathFile) as datafile:
            columnsCsv = csv.reader(datafile, delimiter=';')
            for column in columnsCsv:

                exists = False
                for columnAdded in self.columnsToAdd:
                    if column[1].strip() in columnAdded:
                        exists = True
                        break
                if not exists:
                    self.columnsToAdd.append(column)
                    wsDataNoKeys += ''.rjust(4)+'WSDATA '+ column[1] +' as STRING  OPTIONAL\n'
            
                if column[4] == "1" :
                    defaultVarsKey  += ''.rjust(4)+'Default self:'+ column[1] +' := ""\n'
                    varskey.append(''.rjust(4)+column[1])
                    keyVarsNoKeyPath.append(''.rjust(4)+column[1])
                else:
                    defaultVarsNoKey  += ''.rjust(4)+'Default self:'+ column[1] +' := ""\n'
                    varsNokey.append(''.rjust(4)+column[1])
                
                if column[5] == "1" :
                    keyPath = column[1]
        if len(keyVarsNoKeyPath) > 0:
            keyVarsNoKeyPath.remove('    '+keyPath)
            descriptionPath = self.name.title().replace(" ","")
            descriptionPath = descriptionPath[0].lower() + descriptionPath[1:]
            variables = {
                    'classNameAbreviate': self.shortName,
                    'description': self.name.title(),
                    'descriptionPath': descriptionPath,
                    'className': self.shortName,
                    'classNameLower' : self.shortName.lower(),
                    'entity' : self.entity,
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
        storagePathFile = os.path.join(settings.PATH_FILESTORAGE, self.entity + ".columns")
        variables = self.getVariables(storagePathFile)
        if os.path.isfile(storagePathFile):
            #header
            self.makeTempFile(variables,'Api.Header',"")
            #header.wsdata
            self.makeTempFile(variables,'Api.Header.WsData',self.entity)
            #header.methods
            self.makeTempFile(variables,'Api.Header.Methods',self.entity)
            #footer
            #body
            self.makeTempFile(variables,'Api.Body',self.entity)
        return

    def makeTempFile(self, variables, file, entity):
        fileIn = open(os.path.join(settings.PATH_TEMPLATE, file+'.template'))
        temp = Template(fileIn.read())
        result = temp.substitute(variables)
        f = open(os.path.join(settings.PATH_TEMP, file + entity + ".tmp") , "w+")
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
