# -*- coding: cp1252 -*-
import sys, os, settings, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template
from core.daos.model import Entity, Colunas

class EntityFormComponentTSGenerator(codeGenerator):

    def __init__ (self, entity=None):
        super().__init__(entity=None)
        self.templateFile = 'entity-form.component.ts.template'
        self.templatePath = settings.PATH_TEMPLATE_PO_ENTITY_FORM
        self.srcPath = settings.PATH_PO_SRC_APP
        return

    def setFileOut(self):
        self.fileOut = ""
    
    def getVariables(self):
        optionsVariables = ''
        fields = ''
        descriptionPath = ''
        sufixFileName = '-form.component.ts'
        componentName = self.entity.namePortuguese.title().replace(" ","")
        componentNameLower = componentName.lower()
        componentCammelLower = componentName[:1].lower() + componentName[1:]
        
        self.fileOut = componentNameLower + sufixFileName
        self.srcPath = os.path.join(settings.PATH_PO_SRC_APP,componentNameLower.lower())
        self.srcPath = os.path.join(self.srcPath,componentNameLower.lower()+"-form")
        
        for entity in Entity.select():
            optionsVariables = ''
            fields = ''.rjust(2) + "public readonly fields: Array<PoPageDynamicEditField> = [ \n"
            descriptionPath = self.entity.name.title().replace(" ","")
            descriptionPath = descriptionPath[0].lower() + descriptionPath[1:]
            for column in Colunas.select().join(Entity).where(Entity.table == self.entity.table):
                fields += ''.rjust(4) + "{ property: '" + column.name + "', label: '" + column.desc + "' " 
                fields += ", key: true" if column.is_keyPathParam else ""
                #getting field options
                if column.options != "":
                    fields += ", options: this." + column.name + " "
                    optionsVariables += ''.rjust(2) + "public readonly " + column.name + ": Array<{value: string, label: string}> = [ \n"
                    options = column.options.split(",")
                    for option in options:
                        key = option.split("=")[0]
                        value = option.split("=")[1]
                        optionsVariables += ''.rjust(4) + "{ value: '" + key + "', label: '" + value + "' }, \n"
                    optionsVariables += ''.rjust(2) + "]; \n\n"
                fields += " },\n"
            fields += ''.rjust(2) + "]; \n"

        variables = {
                'componentNameLower' : componentNameLower,
                'componentCammelLower' : componentCammelLower,
                'optionsVariables' : optionsVariables,
                'descriptionPath' : descriptionPath,
                'fields' : fields
            }
        return variables

