# -*- coding: cp1252 -*-
import sys, os, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template
from core.daos.model import Entity, Colunas, Relations
from collections import OrderedDict


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
        dictBodys = {}
        dictBodys['expandables'] = []
        dictBodys['subExpandables'] = []
        keyVariables = ''
        noKeyVariables = '' 
        queryParams = []
        order = []
        body = []
        bodyExpandables = []
        bodySubExpandables = []
        descriptionPath = ''
        defaultVar = ''
        compareValue = ''

        for column in Colunas.select().join(Entity).where(Entity.table == self.entity.table):
            #ajusto a declara��o default da vari�vel
            defaultVar,compareValue = self.getVarName(column)

            compare += ''.rjust(8)+'oResult:assertTrue(oJson["'+ column.name +'"] == '+ compareValue +', "Valor comparado na coluna '+ column.dbField +' de alias '+ column.name +', nao sao iguais. Retorno:" + cRet)  \n'
            compareAll += ''.rjust(8)+'oResult:assertTrue(oJson["items"][1]["'+ column.name +'"] == '+ compareValue +', "Valor comparado na coluna '+ column.dbField +' de alias '+ column.name +', nao sao iguais. Retorno:" + cRet)  \n'
            order.append(column.name)

            if column.dataType == 'float':
                body.append(''.rjust(24)+'\' "'+ column.name +'": \'+AllTrim(Str('+ column.variablename +'))+\'')
            else:
                body.append(''.rjust(24)+'\' "'+ column.name +'": "\'+'+ compareValue +'+\'"')
            
            #B3A_CODIGO;obligationCode;string;3;1;1;C�digo da obriga��o;cCode;;
            if column.is_keyPathParam:
                keyCollumn = column.variablename
            if column.is_indice:
                keyVariables += ''.rjust(4)+'Local '+ column.variablename +' := '+defaultVar+' /*Column ' + column.dbField + '*/\n'
                if not column.is_keyPathParam:
                    queryParams.append(''.rjust(20)+'"&'+ column.name +'="+escape('+ compareValue +')+;')
            else:
                noKeyVariables += ''.rjust(4)+'Local '+ column.variablename +' := '+defaultVar+' /*Column ' + column.dbField + '*/\n'
        
        dictBodys['body'] = body

        for relation in Relations.select().where(Relations.table == self.entity.table):
            for entity in Entity.select().where(Entity.table == relation.tableRelation):
                compare += '\n'
                compare += ''.rjust(8)+'//Expandables\n'
                relationName = entity.name.title().replace(" ","").replace("-","").strip()
                relationName = relationName[0].lower() + relationName[1:]
                for coluna in Colunas.select().where(Colunas.entity_id == entity.id):
                    defaultVar,compareValue = self.getVarName(coluna)
                    compare += ''.rjust(8)+'oResult:assertTrue(oJson["'+ relationName +'"]["'+ coluna.name + '"] == '+ compareValue +', "Valor comparado na coluna '+ coluna.dbField +' de alias '+ coluna.name +', nao sao iguais. Retorno:" + cRet)  \n'
                    if coluna.dataType == 'float':
                        bodyExpandables.append(''.rjust(28)+'\' "'+ coluna.name +'": \'+AllTrim(Str('+ coluna.variabelName +'))+\'')
                    else:
                        bodyExpandables.append(''.rjust(28)+'\' "'+ coluna.name +'": "\'+'+ compareValue +'+\'"')
                
                dictBodys['expandables'].append({ relationName : bodyExpandables })
                
                #Sub relacionamento
                for relation_sub in Relations.select().where(Relations.table == entity.table):
                    for entity_sub in Entity.select().where(Entity.table == relation_sub.tableRelation):
                        compare += '\n'
                        compare += ''.rjust(8)+'//Sub Expandables\n'
                        subRelationName = entity_sub.name.title().replace(" ","").replace("-","").strip()
                        subRelationName = subRelationName[0].lower() + subRelationName[1:]
                        for coluna_sub in Colunas.select().where(Colunas.entity_id == entity_sub.id):
                            defaultVar,compareValue = self.getVarName(coluna_sub)
                            compare += ''.rjust(8)+'oResult:assertTrue(oJson["'+ relationName +'"]["' + subRelationName + '"]["'+ coluna_sub.name + '"] == '+ compareValue +', "Valor comparado na coluna '+ coluna_sub.dbField +' de alias '+ coluna_sub.name +', nao sao iguais. Retorno:" + cRet)  \n'
                            
                            if coluna_sub.dataType == 'float':
                                bodySubExpandables.append(''.rjust(24)+'\' "'+ coluna_sub.name +'": \'+AllTrim(Str('+ coluna_sub.variabelName +'))+\'')
                            else:
                                bodySubExpandables.append(''.rjust(24)+'\' "'+ coluna_sub.name +'": "\'+'+ compareValue +'+\'"')
                            
                        dictBodys['subExpandables'].append({ 
                            relationName : { 
                                subRelationName : bodySubExpandables
                                }
                            })
        
        descriptionPath = self.entity.name.title().replace(" ","")
        descriptionPath = descriptionPath[0].lower() + descriptionPath[1:]
        queryParams = '\n'.join(queryParams)
        order = ','.join(order)
        body = ',\' +;\n'.join(dictBodys['body'])

        #Pode melhorar =)
        for dictBody in dictBodys['expandables']:
            expands = dictBody.keys()
            for expand in expands:
                body += ",'+; \n"+ ''.rjust(24) + "'"' "' + expand + '" : {'+"'+;\n"
                body += ',\'+;\n'.join(dictBody[expand])
                for subDictBody in dictBodys['subExpandables']:
                    subExpands = subDictBody.keys()
                    for subExpand in subExpands:
                        subDicts = subDictBody[subExpand].keys()
                        for subDict in subDicts:
                            if expand == subExpand:
                                body += ",'+; \n"+ ''.rjust(28) + "'"' "' + subDict + '" : {'+"'+;\n        "
                                body += ',\'+;\n        '.join(subDictBody[subExpand].get(subDict))
                                body += "'+;\n"+''.rjust(28)+"'}"

                body += "'+;\n"+''.rjust(24)+"'}"

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
                'body' : body + '\'+;',
            }

        return variables

    def getVarName(self,varName):
        defaultVar = ""
        compareValue = ""
        compareValue = varName.variablename
        if varName.variablename[0].upper() == "C":
            defaultVar = '""'
        elif varName.variablename[0].upper() == "N":
            defaultVar = "0"
        elif varName.variablename[0].upper() == "D":
            defaultVar = 'StoD("")'
            compareValue = 'DtoS('+varName.variablename+')'
        else:
            defaultVar = "Nil"
        
        return defaultVar,compareValue

