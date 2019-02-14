# -*- encoding: utf-8 -*-
import sys, os, settings
from core import managedb, commandController, apiController
from string import Template


class CodeGenerator:

    def builderEntity(self, entity, alias):
        properts  = ''
        gets      = ''
        setters   = ''
        serialize = ''
        fields    = ''

        mdb = managedb.ManagementDb()
        columnInfo = mdb.getColumnInfo(entity)

        for column in columnInfo:
            properts += '    Method get'+ column[0].replace("_", "").capitalize() + '() \n'
            gets     += (
                            'Method get'+ column[0].replace("_", "").capitalize() + '() Class '+ alias + ' \n'
                            'Return self:getValue("' + column[0].replace("_", "").lower() + '") \n\n'
                        )
            serialize   += '    oJsonControl:setProp(oJson,"' + column[0].replace("_", "").lower() + '",self:get'+ column[0].replace("_", "").capitalize() +'()) \n'
            fields      += '    self:oFields:push({"'+column[0].replace("_", "").capitalize()+'", self:get'+ column[0].replace("_", "").capitalize() +'()})\n'

        d = { 
                'className': alias, 
                'properts' : properts, 
                'gets': gets,
                'serialize' : serialize,
                'fields' : fields,
                'entity' : entity,
            }

        
        fileIn = open(os.path.join(settings.PATH_TEMPLATE_ENTITY, 'EntityTempFile.txt'))   
        temp = Template(fileIn.read())
        result = temp.substitute(d)

        f = open(os.path.join(settings.PATH_API_ENTITY, alias.title() + ".prw") , "w+")
        f.write(result)
        f.close()

        return

    def builderDao(entity, alias):
        
        return