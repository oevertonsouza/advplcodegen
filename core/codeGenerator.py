# -*- encoding: utf-8 -*-
import sys, os, settings, csv, shutil
from core import managedb, commandController, apiController
from string import Template


class CodeGenerator:

    def buildEntity(self, entity, name):
        properts  = ''
        gets      = ''
        setters   = ''
        serialize = ''
        fields    = ''

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  entity + ".columns")
        exists = os.path.isfile(storagePathFile)

        if exists:
            with open(storagePathFile) as datafile:
                columnInfo = csv.reader(datafile, delimiter=';')
                for column in columnInfo:
                    properts += '    Method get'+ column[1] + '()\n'
                    gets     += (
                                    'Method get'+ column[1] + '() Class '+ name + '\n'
                                    'Return self:getValue("' + column[1] + '")\n\n'
                                )
                    serialize   += '    oJsonControl:setProp(oJson,"' + column[1].lower() + '",self:get'+ column[1] +'())\n'
                    fields      += '    self:oFields:push({"'+column[1]+'", self:get'+ column[1]+'()})\n'
                    
                d = { 
                        'className': name, 
                        'properts' : properts, 
                        'gets': gets,
                        'serialize' : serialize,
                        'fields' : fields,
                        'entity' : entity,
                    }

                fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'EntityTempFile.txt'))   
                temp = Template(fileIn.read())
                result = temp.substitute(d)

                f = open(os.path.join(settings.PATH_API_ENTITY, name.title() + ".prw") , "w+")
                f.write(result)
                f.close()

                return

    def buildDao(self,entity, name):

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  entity + ".columns")
        exists = os.path.isfile(storagePathFile)

        if exists:
                d = { 
                        'className': name, 
                        'entity' : entity,
                    }

                fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'CollectionTempFile.txt'))
                temp = Template(fileIn.read())
                result = temp.substitute(d)

                f = open(os.path.join(settings.PATH_API_COLLECTION, "Col"+ name.title() + ".prw") , "w+")
                f.write(result)
                f.close()                    

        return

    
    def buildCollection(self,entity, name):

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
                    
                    commit += '        '+alias+'->'+column[0]+' := self:getValue("'+column[1]+'")\n'
                    
                    if column[4] == "1" :
                        bscKey += '    cQuery += " AND ' +column[0]+ ' = "'" + self:getValue('"+column[1]+"') + "'" "\n'
                                    
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

                fileIn = open(os.path.join(settings.PATH_TEMPLATE, 'DaoTempFile.txt'))
                temp = Template(fileIn.read())
                result = temp.substitute(d)

                f = open(os.path.join(settings.PATH_API_DAO, "Dao"+ name.title() + ".prw") , "w+")
                f.write(result)
                f.close()                    

        return

    def copyLibs(self):
        src = settings.PATH_TEMPLATE_LIBS
        dest = settings.PATH_API_LIB
        src_files = os.listdir(src)
        for file_name in src_files:
            full_file_name = os.path.join(src, file_name)
            if (os.path.isfile(full_file_name)):
                shutil.copy(full_file_name, dest)

        return        