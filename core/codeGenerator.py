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

        if exists:
            with open(storagePathFile) as datafile:
                columnInfo = csv.reader(datafile, delimiter=';')
                for column in columnInfo:
                    serialize   += '    oJsonControl:setProp(oJson,"' + column[1] + '",self:get'+ column[1] +'()) /* Column '+ column[0] +' */ \n'
                    fields      += '    self:oFields:push({"'+column[1]+'", self:get'+ column[1]+'()}) /* Column '+ column[0] +' */ \n'
                    
                d = { 
                        'className': name, 
                        'serialize' : serialize,
                        'fields' : fields,
                        'entity' : entity,
                    }

                fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'Entity.template'))   
                temp = Template(fileIn.read())
                result = temp.substitute(d)

                f = open(os.path.join(settings.PATH_SRC_ENTITY, name + ".prw") , "w+")
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

                f = open(os.path.join(settings.PATH_SRC_COLLECTION, "Col"+ name + ".prw") , "w+")
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
                    loadOrder += '    self:oHashOrder:set("'+ column[0] +'", "'+ column[1] +'")\n'
                    
                    commit += '        '+alias+'->'+column[0]+' := self:getValue("'+column[1]+'") /* Column '+ column[0] +' */\n'
                    
                    if column[4] == "1" :
                        cfieldOrder.append(column[0])
                        bscChaPrim += '    xValue = self:getValue("'+column[1]+'")\n'
                        bscChaPrim += '    if !empty(xValue)\n'
                        bscChaPrim += '        cFilter += " AND ' +column[0]+ ' = ? "\n'
                        bscChaPrim += '        aAdd(self:aMapBuilder, self:toString(xValue))\n'
                        bscChaPrim += '    EndIf\n'
                        
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

                f = open(os.path.join(settings.PATH_SRC_DAO, "Dao"+ name + ".prw") , "w+")
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

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  entity + ".columns")
        exists = os.path.isfile(storagePathFile)

        if exists:
            with open(storagePathFile) as datafile:
                columnInfo = csv.reader(datafile, delimiter=';')
                for column in columnInfo:
                    
                    if column[4] == "1":
                        keyValues += '    oCollection:setValue("'+ column[1] +'", "" ) /* Column '+ column[0] +' */ \n'
                    else:
                        noKeyValues +=  '    oCollection:setValue("'+ column[1] +'", "" ) /* Column '+ column[0] +' */ \n'

                d = {
                        'className': name, 
                        'entity' : entity,
                        'alias' : alias,
                        'keyValues' : keyValues,
                        'noKeyValues' : noKeyValues,
                    }

                fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'TestCase.template'))
                temp = Template(fileIn.read())
                result = temp.substitute(d)

                f = open(os.path.join(settings.PATH_SRC_TEST_CASES, name + "TestCase.prw") , "w+")
                f.write(result)
                f.close()

        return

    def buildTestSuite(self,entity, name):

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  entity + ".columns")
        exists = os.path.isfile(storagePathFile)
        
        empresa = settings.PROTHEUS_ENVIORMENT['default']['EMPRESA']
        filial = settings.PROTHEUS_ENVIORMENT['default']['FILIAL']

        d = { 
                'className': name, 
                'entity' : entity,
                'empresa' : empresa,
                'filial' : filial,
            }

        fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'TestSuite.template'))
        temp = Template(fileIn.read())
        result = temp.substitute(d)

        f = open(os.path.join(settings.PATH_SRC_TEST_SUITE, name + "TestSuite.prw") , "w+")
        f.write(result)
        f.close()

        return        

    def buildTestGroup(self,entity, name):

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  entity + ".columns")
        exists = os.path.isfile(storagePathFile)
            
        d = { 
                'className': name, 
                'entity' : entity,
            }

        fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'TestGroup.template'))
        temp = Template(fileIn.read())
        result = temp.substitute(d)

        f = open(os.path.join(settings.PATH_SRC_TEST_GROUP, name + "TestGroup.prw") , "w+")
        f.write(result)
        f.close()

        return

    def buildMapper(self,entity, name):

        mapper = ''

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
                    }

                fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'Mapper.template'))
                temp = Template(fileIn.read())
                result = temp.substitute(d)

                f = open(os.path.join(settings.PATH_SRC_MAPPER, "Mpr"+ name + ".prw") , "w+")
                f.write(result)
                f.close()

        return
    
    def buildRequest(self, entity, name):
        
        alias = entity[:3]
        
        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  entity + ".columns")
        exists = os.path.isfile(storagePathFile)

        d = {
                'className': name,                     
                'entity' : entity,                    
            }

        fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'RestRequest.template'))
        temp = Template(fileIn.read())
        result = temp.substitute(d)

        f = open(os.path.join(settings.PATH_SRC_RESTREQUEST, "Res"+ name +".prw") , "w+")
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