# -*- encoding: utf-8 -*-
import sys, os, settings
from core import managedb, commandController, apiController
from string import Template

class ApiControl:

    def __init__(
                self, 
                apiPath = None, 
                daoPath = None, 
                seekerPath = None, 
                entityPath = None, 
                libPath = None,
                templatePath = None,
                templateEntityPath = None,
            ):

        self.apiPath = os.path.join(settings.PATH_PROJECT, "api")
        self.daoPath = os.path.join(self.apiPath, "dao")
        self.seekerPath = os.path.join(self.apiPath, "seeker")
        self.entityPath = os.path.join(self.apiPath, "entity")
        self.libPath = os.path.join(self.apiPath, "lib")
        self.templatePath = os.path.join(settings.PATH_PROJECT, "templates")
        self.templateEntityPath = os.path.join(self.templatePath, "entity")
        
        return

    def startProject(self):
        
        os.mkdir(self.apiPath)
        os.mkdir(self.daoPath)
        os.mkdir(self.seekerPath)
        os.mkdir(self.entityPath)
        os.mkdir(self.libPath)

        return 

    def newApi(self, entity, alias):
        
        properts = ''
        gets     = ''
        setters  = ''

        mdb = managedb.ManagementDb()
        columnInfo = mdb.getColumnInfo(entity, alias)

        for column in columnInfo:
            properts += '    Method get'+ column[0].replace("_", "").capitalize() + '() \n'
            gets     += (
                            '    Method get'+ column[0].replace("_", "").capitalize() + '() Class '+ alias + ' \n'
                            '    Return self:getValue("' + column[0].replace("_", "").lower() + '") \n\n'
                        )

        className = alias
        d={ 'className': className, 'properts' : properts, 'gets': gets }
        
        fileIn = open(os.path.join(self.templateEntityPath, 'EntityTempFile.txt'))   
        temp = Template(fileIn.read())
        result = temp.substitute(d)

        f = open(os.path.join(self.entityPath , alias.title() + ".prw") , "w+")
        f.write(result)
        f.close()

        #f = open(os.path.join(os.path.join(path, "seeker"), "Skr" + run[2].title()) + ".prw" , "w+")
        #f.close()
        #f = open(os.path.join(os.path.join(path, "entity"), run[2].title()) + ".prw" , "w+")        
        #f.close()
        
        return 