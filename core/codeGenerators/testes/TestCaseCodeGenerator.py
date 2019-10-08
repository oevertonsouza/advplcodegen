# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template
from core.daos.model import Entity, Column

class TestCaseCodeGenerator(codeGenerator):

    def __init__ (self, entity=None):
        super().__init__(entity=None)
        self.templateFile = 'TestCase.template' 
        self.srcPath = settings.PATH_SRC_TEST_CASES
        return

    def setFileOut(self):
        self.fileOut = self.prefix+self.entity.shortName + "TestCase.prw"
    
    def getVariables(self):
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
        for column in Column.select().join(Entity).where(Entity.table == self.entity.table):
            compareValue = column.variabelName
            #ajusto a declaração default da variável
            if column.variabelName[0].upper() == "C":
                defaultVar = '""'
            elif column.variabelName[0].upper() == "N":
                defaultVar = "0"
            elif column.variabelName[0].upper() == "D":
                defaultVar = 'StoD("")'
                compareValue = 'DtoS('+column.variabelName+')'
            else:
                defaultVar = "Nil"

            compare += ''.rjust(8)+'oResult:assertTrue(oJson["'+ column.name +'"] == '+ compareValue +', "Valor comparado na coluna '+ column.dbField +' de alias '+ column.name +', nao sao iguais. Retorno:" + cRet)  \n'
            compareAll += ''.rjust(8)+'oResult:assertTrue(oJson["items"][1]["'+ column.name +'"] == '+ compareValue +', "Valor comparado na coluna '+ column.dbField +' de alias '+ column.name +', nao sao iguais. Retorno:" + cRet)  \n'
            order.append(column.name)
            if column.dataType == 'float':
                body.append(''.rjust(24)+'\' "'+ column.name +'": \'+AllTrim(Str('+ column.variabelName +'))+\'')
            else:
                body.append(''.rjust(24)+'\' "'+ column.name +'": "\'+'+ compareValue +'+\'"')
            #B3A_CODIGO;obligationCode;string;3;1;1;Código da obrigação;cCode;;
            if column.is_keyPathParam:
                keyCollumn = column.variabelName
            if column.is_indice:
                keyVariables += ''.rjust(4)+'Local '+ column.variabelName +' := '+defaultVar+' /*Column ' + column.dbField + '*/\n'
                if not column.is_keyPathParam:
                    queryParams.append(''.rjust(20)+'"&'+ column.name +'="+escape('+ compareValue +')+;')
            else:
                noKeyVariables += ''.rjust(4)+'Local '+ column.variabelName +' := '+defaultVar+' /*Column ' + column.dbField + '*/\n'
            
        descriptionPath = self.entity.name.title().replace(" ","")
        descriptionPath = descriptionPath[0].lower() + descriptionPath[1:]
        queryParams = '\n'.join(queryParams)
        order = ','.join(order)
        body = ',\' +;\n'.join(body)
        variables = {
                'descriptionPath': descriptionPath, 
                'className': self.entity.shortName, 
                'table' : self.entity.table,
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
