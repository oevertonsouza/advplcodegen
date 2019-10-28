# -*- coding: utf-8 -*-
import csv,os,re,sys,shutil
from pathlib import Path
from core.entities import aliasEntity
from core.daos.model import Entity

import settings
from core.codeGenerators.backend import (
                ApiCodeGenerator, CollectionCodeGenerator,
                CommandCodeGenerator, DaoCodeGenerator, DocApiCodeGenerator,
                DocApiSchemaCodeGenerator, MapperCodeGenerator,
                RequestCodeGenerator, ValidateCodeGenerator, entityCodeGenerator
            )
from core.codeGenerators.testes import (
                TestCaseCodeGenerator, TestGroupCodeGenerator, TestSuiteCodeGenerator
            )
from core.codeGenerators.portinari import (
                AppComponentTsGenerator,AppRoutingModuleTsGenerator,
                PackageJsonGenerator,SharedModuleTsGenerator,
                EnvironmentTsGenerator,EntityRoutingModuleTsGenerator,
                EntityModuleTsGenerator,EntityFormComponentCSSGenerator,
                EntityFormComponentHTMLGenerator,EntityFormComponentSpecTSGenerator,
                EntityFormComponentTSGenerator,EntityListComponentCSSGenerator,
                EntityListComponentHTMLGenerator,EntityListComponentSpecTSGenerator,
                EntityListComponentTSGenerator,EntityViewComponentCSSGenerator,
                EntityViewComponentHTMLGenerator,EntityViewComponentSpecTSGenerator,
                EntityViewComponentTSGenerator
            )
from core import storage

class codeGenController:

    def __init__(self):
        return

    def getGenerators(self):
        generators = []
        generators.append(entityCodeGenerator.entityCodeGenerator())
        generators.append(DaoCodeGenerator.DaoCodeGenerator())
        generators.append(CollectionCodeGenerator.CollectionCodeGenerator())
        generators.append(TestCaseCodeGenerator.TestCaseCodeGenerator())
        generators.append(TestGroupCodeGenerator.TestGroupCodeGenerator())
        generators.append(TestSuiteCodeGenerator.TestSuiteCodeGenerator())
        generators.append(MapperCodeGenerator.MapperCodeGenerator())
        generators.append(RequestCodeGenerator.RequestCodeGenerator())
        generators.append(CommandCodeGenerator.CommandCodeGenerator())
        generators.append(ValidateCodeGenerator.ValidateCodeGenerator())
        generators.append(DocApiSchemaCodeGenerator.DocApiSchemaCodeGenerator())
        generators.append(DocApiCodeGenerator.DocApiCodeGenerator())
        generators.append(ApiCodeGenerator.ApiCodeGenerator())

        return generators

    def getPoGenerators(self):
        generators = []
        generators.append(EntityRoutingModuleTsGenerator.EntityRoutingModuleTsGenerator())
        generators.append(EntityModuleTsGenerator.EntityModuleTsGenerator())
        generators.append(EntityFormComponentCSSGenerator.EntityFormComponentCSSGenerator())
        generators.append(EntityFormComponentHTMLGenerator.EntityFormComponentHTMLGenerator())
        generators.append(EntityFormComponentSpecTSGenerator.EntityFormComponentSpecTSGenerator())
        generators.append(EntityFormComponentTSGenerator.EntityFormComponentTSGenerator())
        generators.append(EntityListComponentCSSGenerator.EntityListComponentCSSGenerator())
        generators.append(EntityListComponentHTMLGenerator.EntityListComponentHTMLGenerator())
        generators.append(EntityListComponentSpecTSGenerator.EntityListComponentSpecTSGenerator())
        generators.append(EntityListComponentTSGenerator.EntityListComponentTSGenerator())
        generators.append(EntityViewComponentCSSGenerator.EntityViewComponentCSSGenerator())
        generators.append(EntityViewComponentHTMLGenerator.EntityViewComponentHTMLGenerator())
        generators.append(EntityViewComponentSpecTSGenerator.EntityViewComponentSpecTSGenerator())
        generators.append(EntityViewComponentTSGenerator.EntityViewComponentTSGenerator())
        return generators

    def build(self):

        generators = self.getGenerators()
        for entity in Entity.select():
            new_entity = aliasEntity.AliasEntity(entity.table, entity.name, entity.keyColumn, entity.namePortuguese, entity.shortName)
            for generator in generators:
                generator.setEntity(new_entity)
                generator.build()

        self.finishApi()
        return

    def PoBuild(self):

        generators = self.getPoGenerators()
        AppRoutingModuleTsGenerator.AppRoutingModuleTsGenerator().build()
        AppComponentTsGenerator.AppComponentTsGenerator().build()
        SharedModuleTsGenerator.SharedModuleTsGenerator().build()
        EnvironmentTsGenerator.EnvironmentTsGenerator().build()
        for entity in Entity.select():
            new_entity = aliasEntity.AliasEntity(entity.table, entity.name, entity.keyColumn, entity.namePortuguese, entity.shortName)
            for generator in generators:
                generator.setEntity(new_entity)
                generator.build()
        return

    def PoInstall(self):
        
        print('Instalando Angular')
        os.system('npm uninstall -g @angular/cli')
        os.system('npm cache clean --force')
        os.system('npm i -g @angular/cli')

        print('\nInstalando o projeto my-po-project')
        os.system('ng new my-po-project --skipInstall --interactive=false')

        print('\nCopiando package.json.')
        shutil.copy(settings.PATH_TEMPLATE_PO + '\\package.json', settings.PATH_PO_SRC_APP + '\\package.json')

        print('\nInstalando dependencias')
        os.system('cd '+ settings.PATH_PO +' & npm install')

        print('\nAdiconando o pacote @portinari/portinari-ui')
        os.system('cd '+ settings.PATH_PO +' & npm install @portinari/portinari-ui --defaults=true')

        print('\nAdiconando o pacote @portinari/portinari-templates')
        os.system('cd '+ settings.PATH_PO +' & npm install @portinari/portinari-templates --defaults=true')

        print('\nInicializando o projeto')
        os.system('cd '+ settings.PATH_PO +' & ng serve -o --liveReload=true')

        return
    
    def PoServe(self):
        print('\nInicializando o projeto')
        os.system('cd '+ settings.PATH_PO +' & ng serve -o')

    def openDb(self):
        os.system('cd '+ settings.PATH_DATABASE +' & start sqliteadmin.exe ' + os.path.join(settings.PATH_DATABASE,'advplcodegen.db'))

    def finishApi(self):
        ApiCodeGen = ApiCodeGenerator.ApiCodeGenerator()
        ApiCodeGen.finishApi()

    
