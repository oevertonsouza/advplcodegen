# -*- coding: cp1252 -*-
import sys, os, settings, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template
from core.daos.model import Entity, Column

class DefaultComponentTsGenerator(codeGenerator):

    def __init__ (self, entity=None):
        super().__init__(entity=None)
        self.templateFile = 'default.component.ts.template'
        self.templatePath = settings.PATH_TEMPLATE_PO
        self.srcPath = settings.PATH_PO_SRC_APP
        return

    def setFileOut(self):
        self.fileOut = ""
    
    def getVariables(self):
        fieldsDetails = ''
        sufixFileName = '-dynamic-form.component.ts'
        componentName = self.entity.namePortuguese.replace(" ","").lower()
        className = self.entity.namePortuguese.title().replace(" ","")
        jsonName = className[0].lower() + className[1:]
        self.fileOut = componentName + sufixFileName
        self.srcPath = os.path.join(settings.PATH_PO_SRC_APP,self.entity.namePortuguese.replace(" ","").lower())

        for column in Column.select().join(Entity).where(Entity.table == self.entity.table):
            fieldsDetails += "    { property: '" + column.name + "', "
            fieldsDetails += "          divider: '', "
            fieldsDetails += "          type: '" + column.dataType + "',"
            fieldsDetails += "          required: true, " if column.is_required else "required: false,"
            if column.dataType != 'date':
                fieldsDetails += "          minLength: 0, "
                fieldsDetails += "          maxLength: " + str(column.length) + ", "
            fieldsDetails += "          gridColumns: 6, gridSmColumns: 12 },\n"
        
        variables = {
                'componentName' : componentName,
                'jsonName' : jsonName,
                'className' : className,
                'fieldsDetails' : fieldsDetails
            }
        return variables
