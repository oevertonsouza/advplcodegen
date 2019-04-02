# -*- encoding: utf-8 -*-
import sys, os, settings, csv, shutil
from core import managedb, commandController, apiController
from string import Template


class CodeGenerator:

    def buildEntity(self, entity, name):

        serialize = ''
        fields    = ''

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  entity + ".columns")
        exists = os.path.isfile(storagePathFile)
        prefix = settings.PROTHEUS_ENVIORMENT['default']['PREFIX']

        if exists:
            with open(storagePathFile) as datafile:
                columnInfo = csv.reader(datafile, delimiter=';')
                for column in columnInfo:
                    serialize   += '    oJsonControl:setProp(oJson,"' + column[1] + '",self:getValue("'+ column[1]+'")) /* Column '+ column[0] +' */ \n'
                    fields      += '    self:oFields:push({"'+column[1]+'", self:getValue("'+column[1] +'")}) /* Column '+ column[0] +' */ \n'
                    
                d = { 
                        'className': name, 
                        'serialize' : serialize,
                        'fields' : fields,
                        'entity' : entity,
                        'prefix' : prefix,
                    }

                fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'Entity.template'))   
                temp = Template(fileIn.read())
                result = temp.substitute(d)

                f = open(os.path.join(settings.PATH_SRC_ENTITY, prefix+name + ".prw") , "w+")
                f.write(result)
                f.close()

                return

    def buildCollection(self,entity, name):

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  entity + ".columns")
        prefix = settings.PROTHEUS_ENVIORMENT['default']['PREFIX']

        exists = os.path.isfile(storagePathFile)

        if exists:
                d = { 
                        'className': name, 
                        'entity' : entity,
                        'prefix' : prefix,
                    }

                fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'Collection.template'))
                temp = Template(fileIn.read())
                result = temp.substitute(d)

                f = open(os.path.join(settings.PATH_SRC_COLLECTION, prefix+"Clt"+ name + ".prw") , "w+")
                f.write(result)
                f.close()                    

        return

    
    def buildDao(self,entity, name):

        alias  = entity[:3]
        order  = ''
        table  = ''
        commit = ''
        bscChaPrim = ''
        loadOrder = ''
        cfieldOrder = []
        prefix = settings.PROTHEUS_ENVIORMENT['default']['PREFIX']

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  entity + ".columns")
        exists = os.path.isfile(storagePathFile)

        if exists:
            with open(storagePathFile) as datafile:
                columnInfo = csv.reader(datafile, delimiter=';')

                for column in columnInfo:
                    loadOrder += ''.rjust(4)+'self:oHashOrder:set("'+ column[0] +'", "'+ column[1] +'")\n'
                    
                    commit += ''.rjust(8)+alias+'->'+column[0]+' := _Super:normalizeType('+ alias +'->'+ column[0] +',self:getValue("'+ column[1] +'")) /* Column '+ column[0] +' */\n'
                    
                    if column[4] == "1" :
                        cfieldOrder.append(column[0])
                        bscChaPrim += ''.rjust(4)+'cQuery += " AND ' +column[0]+ ' = ? "\n'
                        bscChaPrim += ''.rjust(4)+'aAdd(self:aMapBuilder, self:toString(self:getValue("'+column[1]+'")))\n'
                        
                d = { 
                        'className': name,
                        'alias': alias,
                        'entity' : entity,
                        'order' : order,
                        'commit': commit,
                        'loadOrder' : loadOrder,
                        'cfieldOrder' : ','.join(cfieldOrder),
                        'bscChaPrim' : bscChaPrim,
                        'prefix' : prefix,
                    }

                fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'Dao.template'))
                temp = Template(fileIn.read())
                result = temp.substitute(d)

                f = open(os.path.join(settings.PATH_SRC_DAO, prefix+"Dao"+ name + ".prw") , "w+")
                f.write(result)
                f.close()

        return

    def buildRequest(self, entity, name):
        
        alias = entity[:3]
        
        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  entity + ".columns")
        exists = os.path.isfile(storagePathFile)
        prefix = settings.PROTHEUS_ENVIORMENT['default']['PREFIX']
        applyFilterAll = ''
        applyFilterSingle = ''
        prepFilter = ''


        if exists:
            with open(storagePathFile) as datafile:
                columnInfo = csv.reader(datafile, delimiter=';')
                for column in columnInfo:
                    applyFilterAll += ''.rjust(12)+'self:oCollection:setValue("'+ column[1] +'",self:oRest:'+ column[1] +')\n'
                    
                    if column[4] == "1" :
                        applyFilterSingle += ''.rjust(12)+'self:oCollection:setValue("'+ column[1] +'",self:oRest:'+ column[1] +')\n'
                        prepFilter += ''.rjust(4)+'self:oRest:'+ column[1] +' := self:oCollection:getValue("'+ column[1] +'")\n'
                      

        d = {
                'className': name,                     
                'entity' : entity, 
                'prefix' : prefix,
                'applyFilterAll' : applyFilterAll,
                'applyFilterSingle' : applyFilterSingle,
                'prepFilter' : prepFilter,
            }

        fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'Request.template'))
        temp = Template(fileIn.read())
        result = temp.substitute(d)

        f = open(os.path.join(settings.PATH_SRC_REQUEST, prefix+"Req"+ name +".prw") , "w+")
        f.write(result)
        f.close()

        return

    def buildApi(self, entity, name):
        
        alias = entity[:3]
        
        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  entity + ".columns")
        exists = os.path.isfile(storagePathFile)
        prefix = settings.PROTHEUS_ENVIORMENT['default']['PREFIX']
        segment = settings.PROTHEUS_ENVIORMENT['default']['SEGMENT']
        wsDataKeys = ''
        wsDataNoKeys = ''
        defaultVarsNoKey = ''
        defaultVarsKey = ''
        varskey = []
        varsNokey = []
        keyVarsNoKeyPath = []
        keyPath = ''
        classNameAbreviate = ''
        

        if exists:
            with open(storagePathFile) as datafile:
                columnInfo = csv.reader(datafile, delimiter=';')
                for column in columnInfo:

                    if column[4] == "1" :
                        defaultVarsKey  += ''.rjust(4)+'Default self:'+ column[1] +' := ""\n'
                        wsDataNoKeys += ''.rjust(4)+'WSDATA '+ column[1] +' as STRING  OPTIONAL\n'
                        varskey.append(''.rjust(4)+column[1])
                        keyVarsNoKeyPath.append(''.rjust(4)+column[1])
                    else:
                        defaultVarsNoKey  += ''.rjust(4)+'Default self:'+ column[1] +' := ""\n'
                        wsDataNoKeys += ''.rjust(4)+'WSDATA '+ column[1] +' as STRING  OPTIONAL\n'
                        varsNokey.append(''.rjust(4)+column[1])
                    
                    if column[5] == "1" :
                        keyPath = column[1]

        keyVarsNoKeyPath.remove('    '+keyPath)

        d = {
                'classNameAbreviate': name[:4],
                'className': name,                     
                'classNameLower' : name.lower(),
                'entity' : entity, 
                'prefix' : prefix,
                'segment' : segment,
                'wsDataKeys' : wsDataKeys,
                'wsDataNoKeys' : wsDataNoKeys,
                'defaultVarsKey' : defaultVarsKey,
                'defaultVarsNoKey' : defaultVarsNoKey,
                'varskey' : ',;\n'.join(varskey)+',;',
                'varsNokey' : ',;\n'.join(varsNokey)+';',
                'keyPath' : keyPath,
                'keyVarsNoKeyPath' : ';\n'.join(keyVarsNoKeyPath)+';',
            }

        fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'Api.template'))
        temp = Template(fileIn.read())
        result = temp.substitute(d)

        f = open(os.path.join(settings.PATH_SRC_API, prefix+"Rest"+ segment +".prw") , "w+")
        f.write(result)
        f.close()

        return                

    def buildTest(self,entity, name):
        self.buildTestGroup(entity, name)
        self.buildTestSuite(entity, name)
        self.buildTestCase(entity, name)
        return
    
    def buildTestCase(self,entity, name):

        keyValues = ''
        noKeyValues = ''
        alias = entity[:3]
        prefix = settings.PROTHEUS_ENVIORMENT['default']['PREFIX']
        compare = ''
        changeValues = ''
        keyVariables = ''
        noKeyVariables = ''
        cleanVarCollection = ''
        
        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  entity + ".columns")
        exists = os.path.isfile(storagePathFile)

        if exists:
            with open(storagePathFile) as datafile:
                columnInfo = csv.reader(datafile, delimiter=';')
                for column in columnInfo:
                    
                    if column[4] == "1":
                        keyValues += ''.rjust(4)+'oCollection:setValue("'+ column[1] +'", '+column[1]+' ) /* Column '+ column[0] +' */ \n'
                        keyVariables += ''.rjust(4)+'Local '+ column[1] +' := Nil\n'
                    else:
                        noKeyVariables += ''.rjust(4)+'Local '+ column[1] +' := Nil\n'
                        noKeyValues +=  ''.rjust(4)+'oCollection:setValue("'+ column[1] +'", '+column[1]+' ) /* Column '+ column[0] +' */ \n'
                        changeValues += ''.rjust(8)+'o'+prefix+name+':setValue("'+ column[1] +'", '+ column[1] +')  /* Column '+ column[0] +' */ \n'
                        compare += ''.rjust(8)+'oResult:assertTrue(oCenProducts:getValue("'+ column[1] +'") == '+ column[1] +', "Valor comparado na coluna '+ column[0] +' de alias '+ column[1] +', nao sao iguais.")  /* Column '+ column[0] +' */ \n'
                        cleanVarCollection += ''.rjust(4)+column[1]+' := ""\n'

                d = {
                        'className': name, 
                        'entity' : entity,
                        'alias' : alias,
                        'keyValues' : keyValues,
                        'noKeyValues' : noKeyValues,
                        'prefix' : prefix,
                        'compare' : compare,
                        'changeValues' : changeValues,
                        'keyVariables' : keyVariables,
                        'noKeyVariables' : noKeyVariables,
                        'cleanVarCollection' : cleanVarCollection,
                    }

                fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'TestCase.template'))
                temp = Template(fileIn.read())
                result = temp.substitute(d)

                f = open(os.path.join(settings.PATH_SRC_TEST_CASES, prefix+name + "TestCase.prw") , "w+")
                f.write(result)
                f.close()

        return

    def buildTestSuite(self,entity, name):

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  entity + ".columns")
        exists = os.path.isfile(storagePathFile)
        
        empresa = settings.PROTHEUS_ENVIORMENT['default']['EMPRESA']
        filial = settings.PROTHEUS_ENVIORMENT['default']['FILIAL']
        prefix = settings.PROTHEUS_ENVIORMENT['default']['PREFIX']

        d = { 
                'className': name, 
                'entity' : entity,
                'empresa' : empresa,
                'filial' : filial,
                'prefix' : prefix,
            }

        fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'TestSuite.template'))
        temp = Template(fileIn.read())
        result = temp.substitute(d)

        f = open(os.path.join(settings.PATH_SRC_TEST_SUITE, prefix+name + "TestSuite.prw") , "w+")
        f.write(result)
        f.close()

        return        

    def buildTestGroup(self,entity, name):

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  entity + ".columns")
        exists = os.path.isfile(storagePathFile)
        prefix = settings.PROTHEUS_ENVIORMENT['default']['PREFIX']
            
        d = { 
                'className': name, 
                'entity' : entity,
                'prefix' : prefix,
            }

        fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'TestGroup.template'))
        temp = Template(fileIn.read())
        result = temp.substitute(d)

        f = open(os.path.join(settings.PATH_SRC_TEST_GROUP, prefix+name + "TestGroup.prw") , "w+")
        f.write(result)
        f.close()

        return

    def buildMapper(self,entity, name):

        mapper = ''
        prefix = settings.PROTHEUS_ENVIORMENT['default']['PREFIX']

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  entity + ".columns")
        exists = os.path.isfile(storagePathFile)

        if exists:
            with open(storagePathFile) as datafile:
                columnInfo = csv.reader(datafile, delimiter=';')
                for column in columnInfo:
                    mapper += '    aAdd(self:aFields,{"'+ column[0] +'" ,"'+ column[1] +'"})\n'
                
                d = { 
                        'className': name, 
                        'entity' : entity,
                        'mapper' : mapper,
                        'prefix' : prefix,
                    }

                fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'Mapper.template'))
                temp = Template(fileIn.read())
                result = temp.substitute(d)

                f = open(os.path.join(settings.PATH_SRC_MAPPER, prefix+"Mpr"+ name + ".prw") , "w+")
                f.write(result)
                f.close()

        return
    
    def buildCommand(self, entity, name):
        
        prefix = settings.PROTHEUS_ENVIORMENT['default']['PREFIX']
        
        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  entity + ".columns")
        exists = os.path.isfile(storagePathFile)

        d = {
                'className': name,                     
                'entity' : entity,                    
                'prefix' : prefix,
            }

        fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'Command.template'))
        temp = Template(fileIn.read())
        result = temp.substitute(d)

        f = open(os.path.join(settings.PATH_SRC_COMMAND, prefix+"Cmd"+ name +".prw") , "w+")
        f.write(result)
        f.close()

        return

    def buildValidate(self, entity, name):
        
        prefix = settings.PROTHEUS_ENVIORMENT['default']['PREFIX']
        
        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  entity + ".columns")
        exists = os.path.isfile(storagePathFile)

        d = {
                'className': name,
                'entity' : entity,                    
                'prefix' : prefix,
            }

        fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'Validator.template'))
        temp = Template(fileIn.read())
        result = temp.substitute(d)

        f = open(os.path.join(settings.PATH_SRC_VALIDATE, prefix+"Vld"+ name +".prw") , "w+")
        f.write(result)
        f.close()

        return        

    def copyLibs(self):
        
        prefix = settings.PROTHEUS_ENVIORMENT['default']['PREFIX']
        dest = settings.PATH_SRC_LIB
        src_files = os.listdir(settings.PATH_TEMPLATE_LIBS)
        for file_name in src_files:
            fileIn = open(os.path.join(settings.PATH_TEMPLATE_LIBS, file_name))
            temp = Template(fileIn.read())
            result = temp.substitute({'prefix': prefix})
            fileIn.close()
            file = file_name.split('.')
            f = open(os.path.join(settings.PATH_SRC_LIB, prefix+file[0]+'.prw' ) , "w+")
            f.write(result)
            f.close()
            
        return        
