# -*- coding: cp1252 -*-
import sys, os, settings, csv, shutil
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template

class TestCaseCodeGenerator(codeGenerator):

    def __init__ (self, entity=None, name=None, alias=None, shortName=None):
        super().__init__(entity=None, name=None, alias=None, shortName=None)
        self.templateFile = 'TestCase.template' 
        self.srcPath = settings.PATH_SRC_TEST_CASES
        return

    def setFileOut(self):
        self.fileOut = self.prefix+self.shortName + "TestCase.prw"
    
    def getVariables(self,storagePathFile):
        keyCollumn = ''
        compare = ''
        compareAll = ''
        keyVariables = ''
        noKeyVariables = ''
        queryParams = []
        order = []
        body = []
        descriptionPath = ''
        defaultVar = ''
        compareValue = ''

        with open(storagePathFile) as datafile:
            columnInfo = csv.reader(datafile, delimiter=';')
            for column in columnInfo:
                compareValue = column[7]
                #ajusto a declaração default da variável
                if column[7][0].upper() == "C":
                    defaultVar = '""'
                elif column[7][0].upper() == "N":
                    defaultVar = "0"
                elif column[7][0].upper() == "D":
                    defaultVar = 'StoD("")'
                    compareValue = 'DtoS('+column[7]+')'
                else:
                    defaultVar = "Nil"

                compare += ''.rjust(8)+'oResult:assertTrue(oJson["'+ column[1] +'"] == '+ compareValue +', "Valor comparado na coluna '+ column[0] +' de alias '+ column[1] +', nao sao iguais. Retorno:" + cRet)  \n'
                compareAll += ''.rjust(8)+'oResult:assertTrue(oJson["items"][1]["'+ column[1] +'"] == '+ compareValue +', "Valor comparado na coluna '+ column[0] +' de alias '+ column[1] +', nao sao iguais. Retorno:" + cRet)  \n'
                order.append(column[1])
                if column[2] == 'float':
                    body.append(''.rjust(24)+'\' "'+ column[1] +'": \'+AllTrim(Str('+ column[7] +'))+\'')
                else:
                    body.append(''.rjust(24)+'\' "'+ column[1] +'": "\'+'+ compareValue +'+\'"')

                if column[5] == "1":
                    keyCollumn = column[7]
                if column[4] == "1":
                    keyVariables += ''.rjust(4)+'Local '+ column[7] +' := '+defaultVar+' /*Column ' + column[0] + '*/\n'
                    if column[5] == "0":
                        queryParams.append(''.rjust(20)+'"&'+ column[1] +'="+escape('+ compareValue +')+;')
                else:
                    noKeyVariables += ''.rjust(4)+'Local '+ column[7] +' := '+defaultVar+' /*Column ' + column[0] + '*/\n'
            
            descriptionPath = self.name.title().replace(" ","")
            descriptionPath = descriptionPath[0].lower() + descriptionPath[1:]
            queryParams = '\n'.join(queryParams)
            order = ','.join(order)
            body = ',\' +;\n'.join(body)
            variables = {
                    'descriptionPath': descriptionPath, 
                    'className': self.shortName, 
                    'entity' : self.entity,
                    'alias' : self.alias,
                    'prefix' : self.prefix,
                    'compare' : compare,
                    'compareAll' : compareAll,
                    'keyVariables' : keyVariables,
                    'noKeyVariables' : noKeyVariables,
                    'queryParams' : queryParams,
                    'keyCollumn' : keyCollumn,
                    'order' : order,
                    'body' : body + '\' +;',
                }

        return variables
