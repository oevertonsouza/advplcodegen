# -*- coding: cp1252 -*-
import sys, os, settings, csv, shutil
from core import managedb, commandController, apiController
from string import Template


class CodeGenerator():

    prefix  = settings.PROTHEUS_ENVIORMENT['default']['PREFIX']
    product = settings.PROTHEUS_ENVIORMENT['default']['PRODUCT']
    productDescription = settings.PROTHEUS_ENVIORMENT['default']['PRDUCT_DESCRIPTION']
    contact = settings.PROTHEUS_ENVIORMENT['default']['CONTACT']
    segment = settings.PROTHEUS_ENVIORMENT['default']['SEGMENT']
    company = settings.PROTHEUS_ENVIORMENT['default']['COMPANY']
    filial = settings.PROTHEUS_ENVIORMENT['default']['FILIAL']

    def __init__ (self, entity=None, name=None, alias=None):
        self.entity = entity, 
        self.name = name,
        self.alias = alias,
        return

    def setEntity(self, entity):
        self.entity = entity
        self.alias = entity[:3]
        return

    def setName(self, name):
        self.name = name
        return

    def buildEntity(self):

        serialize = ''
        fields    = ''

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  self.entity + ".columns")
        exists = os.path.isfile(storagePathFile)

        if exists:
            with open(storagePathFile) as datafile:
                columnInfo = csv.reader(datafile, delimiter=';')
                for column in columnInfo:
                    serialize   += '    oJsonControl:setProp(oJson,"' + column[1] + '",self:getValue("'+ column[1]+'")) /* Column '+ column[0] +' */ \n'
                    fields      += '    self:oFields:push({"'+column[1]+'", self:getValue("'+column[1] +'")}) /* Column '+ column[0] +' */ \n'
                    
                d = { 
                        'className': self.name, 
                        'serialize' : serialize,
                        'fields' : fields,
                        'entity' : self.entity,
                        'prefix' : self.prefix,
                    }

                fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'Entity.template'))   
                temp = Template(fileIn.read())
                result = temp.substitute(d)

                f = open(os.path.join(settings.PATH_SRC_ENTITY, self.prefix+self.name + ".prw") , "w+")
                f.write(result)
                f.close()

                return

    def buildCollection(self):

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  self.entity + ".columns")
        exists = os.path.isfile(storagePathFile)

        if exists:
                d = { 
                        'className': self.name, 
                        'entity' : self.entity,
                        'prefix' : self.prefix,
                    }

                fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'Collection.template'))
                temp = Template(fileIn.read())
                result = temp.substitute(d)

                f = open(os.path.join(settings.PATH_SRC_COLLECTION, self.prefix+"Clt"+ self.name + ".prw") , "w+")
                f.write(result)
                f.close()                    

        return

    
    def buildDao(self):

        commitKey = ''
        commitNoKey = ''
        bscChaPrim = ''
        loadOrder = ''
        cfieldOrder = []

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  self.entity + ".columns")
        exists = os.path.isfile(storagePathFile)

        if exists:
            with open(storagePathFile) as datafile:
                columnInfo = csv.reader(datafile, delimiter=';')

                for column in columnInfo:
                    loadOrder += ''.rjust(4)+'self:oHashOrder:set("'+ column[0] +'", "'+ column[1] +'")\n'
                    
                    if column[4] == "1" :
                        cfieldOrder.append(column[0])
                        commitKey += ''.rjust(12)+self.alias+'->'+column[0]+' := _Super:normalizeType('+ self.alias +'->'+ column[0] +',self:getValue("'+ column[1] +'")) /* Column '+ column[0] +' */\n'
                        bscChaPrim += ''.rjust(4)+'cQuery += " AND ' +column[0]+ ' = ? "\n'
                        bscChaPrim += ''.rjust(4)+'aAdd(self:aMapBuilder, self:toString(self:getValue("'+column[1]+'")))\n'
                    else:
                        commitNoKey += ''.rjust(8)+self.alias+'->'+column[0]+' := _Super:normalizeType('+ self.alias +'->'+ column[0] +',self:getValue("'+ column[1] +'")) /* Column '+ column[0] +' */\n'
                        
                d = { 
                        'className': self.name,
                        'alias': self.alias,
                        'entity' : self.entity,
                        'commitKey' : commitKey,
                        'commitNoKey' : commitNoKey,
                        'loadOrder' : loadOrder,
                        'cfieldOrder' : ','.join(cfieldOrder),
                        'bscChaPrim' : bscChaPrim,
                        'prefix' : self.prefix,
                    }

                fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'Dao.template'))
                temp = Template(fileIn.read())
                result = temp.substitute(d)

                f = open(os.path.join(settings.PATH_SRC_DAO, self.prefix+"Dao"+ self.name + ".prw") , "w+")
                f.write(result)
                f.close()

        return

    def buildRequest(self):
        
        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  self.entity+".columns")
        exists = os.path.isfile(storagePathFile)
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
                        prepFilter += ''.rjust(4)+'self:oCollection:setValue("'+ column[1] +'", self:oRest:'+ column[1] +')\n'

        d = {
                'className': self.name,                     
                'entity' : self.entity,
                'prefix' : self.prefix,
                'applyFilterAll' : applyFilterAll,
                'applyFilterSingle' : applyFilterSingle,
                'prepFilter' : prepFilter,
            }

        fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'Request.template'))
        temp = Template(fileIn.read())
        result = temp.substitute(d)

        f = open(os.path.join(settings.PATH_SRC_REQUEST, self.prefix+"Req"+ self.name +".prw") , "w+")
        f.write(result)
        f.close()

        return

    def buildApi(self):
        
        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  self.entity + ".columns")
        exists = os.path.isfile(storagePathFile)
        wsDataKeys = ''
        wsDataNoKeys = ''
        defaultVarsNoKey = ''
        defaultVarsKey = ''
        varskey = []
        varsNokey = []
        keyVarsNoKeyPath = []
        keyPath = ''

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
                'classNameAbreviate': self.name[:4],
                'className': self.name,
                'classNameLower' : self.name.lower(),
                'entity' : self.entity,
                'prefix' : self.prefix,
                'segment' : self.segment,
                'wsDataKeys' : wsDataKeys,
                'wsDataNoKeys' : wsDataNoKeys,
                'defaultVarsKey' : defaultVarsKey,
                'defaultVarsNoKey' : defaultVarsNoKey,
                'varskey' : ',;\n'.join(varskey)+',;',
                'varsNokey' : ',;\n'.join(varsNokey)+';',
                'keyPath' : keyPath,
                'keyVarsNoKeyPath' : ',;\n'.join(keyVarsNoKeyPath)+';',
            }

        #header
        fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'Api.Header.template'))
        temp = Template(fileIn.read())
        result = temp.substitute(d)
        f = open(os.path.join(settings.PATH_TEMP, "Api.Header.tmp") , "w+")
        f.write(result)
        f.close()
        #header.wsdata
        fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'Api.Header.WsData.template'))
        temp = Template(fileIn.read())
        result = temp.substitute(d)
        f = open(os.path.join(settings.PATH_TEMP, "Api.Header.WsData."+ self.entity +".tmp") , "w+")
        f.write(result)
        f.close()
        #header.methods
        fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'Api.Header.Methods.template'))
        temp = Template(fileIn.read())
        result = temp.substitute(d)
        f = open(os.path.join(settings.PATH_TEMP, "Api.Header.Methods."+ self.entity +".tmp") , "w+")
        f.write(result)
        f.close()
        #footer
        #body
        fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'Api.Body.template'))
        temp = Template(fileIn.read())
        result = temp.substitute(d)
        f = open(os.path.join(settings.PATH_TEMP, "Api.Body."+ self.entity +".tmp") , "w+")
        f.write(result)
        f.close()

        return                

    def finishApi(self):
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
        f = open(os.path.join(settings.PATH_SRC_API, self.prefix+"Rest"+ self.segment +".prw") , "w+")
        f.write(result)
        f.close()

    def buildTest(self):
        self.buildTestGroup()
        self.buildTestSuite()
        self.buildTestCase()
        return
    
    def buildTestCase(self):

        keyValues = ''
        noKeyValues = ''
        compare = ''
        changeValues = ''
        keyVariables = ''
        noKeyVariables = ''
        cleanVarCollection = ''
        
        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  self.entity + ".columns")
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
                        changeValues += ''.rjust(8)+'o'+self.prefix+self.name+':setValue("'+ column[1] +'", '+ column[1] +')  /* Column '+ column[0] +' */ \n'
                        compare += ''.rjust(8)+'oResult:assertTrue(oCenProducts:getValue("'+ column[1] +'") == '+ column[1] +', "Valor comparado na coluna '+ column[0] +' de alias '+ column[1] +', nao sao iguais.")  /* Column '+ column[0] +' */ \n'
                        cleanVarCollection += ''.rjust(4)+column[1]+' := ""\n'

                d = {
                        'className': self.name, 
                        'entity' : self.entity,
                        'alias' : self.alias,
                        'keyValues' : keyValues,
                        'noKeyValues' : noKeyValues,
                        'prefix' : self.prefix,
                        'compare' : compare,
                        'changeValues' : changeValues,
                        'keyVariables' : keyVariables,
                        'noKeyVariables' : noKeyVariables,
                        'cleanVarCollection' : cleanVarCollection,
                    }

                fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'TestCase.template'))
                temp = Template(fileIn.read())
                result = temp.substitute(d)

                f = open(os.path.join(settings.PATH_SRC_TEST_CASES, self.prefix+self.name + "TestCase.prw") , "w+")
                f.write(result)
                f.close()

        return

    def buildTestSuite(self):

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  self.entity + ".columns")
        if os.path.isfile(storagePathFile):
            d = { 
                    'className': self.name, 
                    'entity' : self.entity,
                    'company' : self.company,
                    'filial' : self.filial,
                    'prefix' : self.prefix,
                }

            fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'TestSuite.template'))
            temp = Template(fileIn.read())
            result = temp.substitute(d)

            f = open(os.path.join(settings.PATH_SRC_TEST_SUITE, self.prefix+self.name + "TestSuite.prw") , "w+")
            f.write(result)
            f.close()

        return        

    def buildTestGroup(self):

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE , self.entity + ".columns")
        if os.path.isfile(storagePathFile):
            d = { 
                    'className': self.name, 
                    'entity' : self.entity,
                    'prefix' : self.prefix,
                }

            fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'TestGroup.template'))
            temp = Template(fileIn.read())
            result = temp.substitute(d)

            f = open(os.path.join(settings.PATH_SRC_TEST_GROUP, self.prefix+self.name + "TestGroup.prw") , "w+")
            f.write(result)
            f.close()
        return

    def buildMapper(self):

        mapper = ''
        storagePathFile = os.path.join(settings.PATH_FILESTORAGE, self.entity + ".columns")
        exists = os.path.isfile(storagePathFile)

        if exists:
            with open(storagePathFile) as datafile:
                columnInfo = csv.reader(datafile, delimiter=';')
                for column in columnInfo:
                    mapper += '    aAdd(self:aFields,{"'+ column[0] +'" ,"'+ column[1] +'"})\n'
                
                d = { 
                        'className': self.name, 
                        'entity' : self.entity,
                        'mapper' : mapper,
                        'prefix' : self.prefix,
                    }

                fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'Mapper.template'))
                temp = Template(fileIn.read())
                result = temp.substitute(d)

                f = open(os.path.join(settings.PATH_SRC_MAPPER, self.prefix+"Mpr"+ self.name + ".prw") , "w+")
                f.write(result)
                f.close()

        return

    def buildDocApiSchema(self):

        propertiesKey = ''
        propertiesNoKey = ''

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  self.entity + ".columns")
        exists = os.path.isfile(storagePathFile)

        if exists:
            with open(storagePathFile) as datafile:
                columnInfo = csv.reader(datafile, delimiter=';')
                for column in columnInfo:
                    if column[4] == "1":
                        propertiesKey += ''.rjust(16)+(
                            '"'+column[1]+'": {\n'
				            '                    "description": "Descrição do campo",\n'
                            '                    "type": "string",\n'
                            '                    "x-totvs": [\n'
                            '		                {\n'
                            '                           "product": "'+ self.product +'",\n'
                            '                           "field": "'+ self.alias +'.'+column[0]+'",\n'
                            '                           "required": false,\n'
                            '                           "type": "string",\n'
                            '                           "length": "'+column[3]+'",\n'
                            '                           "note": "Descrição do campo",\n'
                            '                           "available": true,\n'
                            '                           "canUpdate": false\n'                            
                            '                        }\n'
                            '                   ]\n'
                            '                },\n'
                        )
                    else:
                        propertiesNoKey += ''.rjust(16)+(
                            '"'+column[1]+'": {\n'
				            '                    "description": "Descrição do campo",\n'
                            '                    "type": "string",\n'
                            '                    "x-totvs": [\n'
                            '		                {\n'
                            '                           "product": "'+ self.product +'",\n'
                            '                           "field": "'+ self.alias +'.'+column[0]+'",\n'
                            '                           "required": false,\n'
                            '                           "type": "string",\n'
                            '                           "length": "'+column[3]+'",\n'
                            '                           "note": "Descrição do campo",\n'
                            '                           "available": true,\n'
                            '                           "canUpdate": true\n'                            
                            '                        }\n'
                            '                   ]\n'
                            '                },\n'
                        )
                
                d = { 
                        'className': self.name, 
                        'entity' : self.entity,
                        'product' : self.product,
                        'productDescription' : self.productDescription,
                        'contact' : self.contact,
                        'segment' : self.segment,
                        'propertiesKey' : propertiesKey[:-1],
                        'propertiesNoKey' : propertiesNoKey[:-2],
                        'classNameLower' : self.name.lower(),
                    }

                fileIn = open(os.path.join(settings.PATH_TEMPLATE_DOCS, 'docApiSchema.template'))
                temp = Template(fileIn.read())
                result = temp.substitute(d)

                f = open(os.path.join(settings.PATH_SRC_DOC, self.name+"_1_100.json") , "w+")
                f.write(result)
                f.close()

        return

    def buildDocApi(self):

        pathParam = ''
        queryParam = ''
        parameters = ''
        keyParameters = ''
        keyPath = ''
        abreviate = self.name[:4]

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  self.entity + ".columns")
        exists = os.path.isfile(storagePathFile)

        if exists:
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
			                        	'               "description": "Descricao do Campo",\n'
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
			                            	'               "description": "Descricao do Campo",\n'
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
			                                '               "description": "Descricao do Campo",\n'
			                                '               "required": false,\n'
			                                '               "schema": {\n'
    			                            '		            "type": "string",\n'
			                                '	                "format": "string"\n'
			                                '               }\n'
			                                '           },\n'
                            )

                d = { 
                        'className': self.name, 
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

                fileIn = open(os.path.join(settings.PATH_TEMPLATE_DOCS, 'docApi.template'))
                temp = Template(fileIn.read())
                result = temp.substitute(d)

                f = open(os.path.join(settings.PATH_SRC_DOC, self.name+"_v1_100.json") , "w+")
                f.write(result)
                f.close()

        return    
    
    def buildCommand(self):
        
        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  self.entity + ".columns")
        if os.path.isfile(storagePathFile):

            d = {
                    'className': self.name,                     
                    'entity' : self.entity,
                    'prefix' : self.prefix,
                }

            fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'Command.template'))
            temp = Template(fileIn.read())
            result = temp.substitute(d)

            f = open(os.path.join(settings.PATH_SRC_COMMAND, self.prefix+"Cmd"+ self.name +".prw") , "w+")
            f.write(result)
            f.close()

        return

    def buildValidate(self):
        
        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  self.entity + ".columns")
        if os.path.isfile(storagePathFile):

            d = {
                    'className': self.name,
                    'entity' : self.entity,                    
                    'prefix' : self.prefix,
                }

            fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'Validator.template'))
            temp = Template(fileIn.read())
            result = temp.substitute(d)

            f = open(os.path.join(settings.PATH_SRC_VALIDATE, self.prefix+"Vld"+ self.name +".prw") , "w+")
            f.write(result)
            f.close()

        return

    def copyLibs(self):
        
        src_files = os.listdir(settings.PATH_TEMPLATE_LIBS)
        for file_name in src_files:
            fileIn = open(os.path.join(settings.PATH_TEMPLATE_LIBS, file_name))
            temp = Template(fileIn.read())
            result = temp.substitute({'prefix': self.prefix})
            fileIn.close()
            file = file_name.split('.')
            f = open(os.path.join(settings.PATH_SRC_LIB, self.prefix+file[0]+'.prw' ) , "w+")
            f.write(result)
            f.close()
            
        return        
