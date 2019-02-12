# -*- encoding: utf-8 -*-
import sys, os, settings
from core import managedb, commandController, apiController
from string import Template


class CodeGenerator:

    def builderEntity(self, path, entity, alias):
        properts  = ''
        gets      = ''
        setters   = ''
        serialize = ''
        fields    = ''

        mdb = managedb.ManagementDb()
        columnInfo = mdb.getColumnInfo(entity, alias)

        for column in columnInfo:
            properts += '    Method get'+ column[0].replace("_", "").capitalize() + '() \n'
            gets     += (
                            'Method get'+ column[0].replace("_", "").capitalize() + '() Class '+ alias + ' \n'
                            'Return self:getValue("' + column[0].replace("_", "").lower() + '") \n\n'
                        )
            serialize   += '    oJsonControl:setProp(oJson,"' + column[0].replace("_", "").lower() + '",self:get'+ column[0].replace("_", "").capitalize() +'()) \n'
            fields      += '    self:oFields:push({"'+column[0].replace("_", "").capitalize()+'", self:get'+ column[0].replace("_", "").capitalize() +'()})\n'
        
        className = alias
        
        d = { 
                'className': className, 
                'properts' : properts, 
                'gets': gets,
                'serialize' : serialize,
                'fields' : fields,
            }

        
        fileIn = open(os.path.join(self.templateEntityPath, 'EntityTempFile.txt'))   
        temp = Template(fileIn.read())
        result = temp.substitute(d)

        f = open(os.path.join(self.entityPath , alias.title() + ".prw") , "w+")
        f.write(result)
        f.close()

        return

    def builderDao(entity, alias):
        
        return