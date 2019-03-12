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
        exists = os.path.isfile(storagePathFile)

        if exists:
                d = { 
                        'className': name, 
                        'entity' : entity,
                    }

                fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'Collection.template'))
                temp = Template(fileIn.read())
                result = temp.substitute(d)

                f = open(os.path.join(settings.PATH_SRC_COLLECTION, "Col"+ name + ".prw") , "w+")
                f.write(result)
                f.close()                    

        return

    
    def buildDao(self,entity, name):

        fields = ''
        alias  = entity[:3]
        order  = ''
        table  = ''
        getFielters = ''  
        commit = ''
        bscKey = ''

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  entity + ".columns")
        exists = os.path.isfile(storagePathFile)

        if exists:
            with open(storagePathFile) as datafile:
                columnInfo = csv.reader(datafile, delimiter=';')
                for column in columnInfo:
                    fields += '        self:cFields += " '+column[0].upper()+', "\n'
                    
                    getFielters += '    xValue := self:getValue("'+column[1]+'")\n'
                    getFielters += '    if !empty(xValue)\n'
                    getFielters += '        cFilter += " AND '+column[0].upper()+' = ? "\n'
                    getFielters += '        aAdd(self:aMapBuilder, self:toString(xValue))\n'
                    getFielters += '    EndIf\n'
                    
                    commit += '        '+alias+'->'+column[0]+' := self:getValue("'+column[1]+'") /* Column '+ column[0] +' */\n'
                    
                    if column[4] == "1" :
                        bscKey += '    xValue = self:getValue("'+column[1]+'")\n'
                        bscKey += '    if !empty(xValue)\n'
                        bscKey += '        cFilter += " AND ' +column[0]+ ' = ? "\n'
                        bscKey += '        aAdd(self:aMapBuilder, self:toString(xValue))\n'
                        bscKey += '    EndIf\n'
                                    
                d = { 
                        'className': name, 
                        'fields' : fields, 
                        'alias': alias,
                        'entity' : entity,
                        'order' : order,
                        'getFielters': getFielters,
                        'commit': commit,
                        'bscKey': bscKey,
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

        deleteValues = ''
        alias = entity[:3]

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  entity + ".columns")
        exists = os.path.isfile(storagePathFile)

        if exists:
            with open(storagePathFile) as datafile:
                columnInfo = csv.reader(datafile, delimiter=';')
                for column in columnInfo:
                    if column[4] == "1":
                        deleteValues += '    oCollection:setValue("'+ column[1] +'", "" ) /* Column '+ column[0] +' */ \n'
                    
                d = { 
                        'className': name, 
                        'entity' : entity,
                        'deleteValues' : deleteValues,
                        'alias' : alias,
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

        mapFromDao = ''

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  entity + ".columns")
        exists = os.path.isfile(storagePathFile)

        if exists:
            with open(storagePathFile) as datafile:
                columnInfo = csv.reader(datafile, delimiter=';')
                for column in columnInfo:            
                    mapFromDao += '    self:oEntity:setValue("'+ column[1] +'", AllTrim((oDao:cAliasTemp)->'+ column[0] +'))\n'
                
                d = { 
                        'className': name, 
                        'entity' : entity,
                        'mapFromDao' : mapFromDao,
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
        src = settings.PATH_TEMPLATE_LIBS
        dest = settings.PATH_SRC_LIB
        src_files = os.listdir(src)
        for file_name in src_files:
            full_file_name = os.path.join(src, file_name)
            if (os.path.isfile(full_file_name)):
                shutil.copy(full_file_name, dest)

        return        