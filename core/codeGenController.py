# -*- coding: utf-8 -*-
import csv,os,re,sys
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
                DefaultComponentHtmlGenerator, PackageJsonGenerator,
                DefaultComponentTsGenerator, AppModuleTsGenerator
                #DefaultModuleTsGenerator
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
        generators.append(DefaultComponentHtmlGenerator.DefaultComponentHtmlGenerator())
        generators.append(DefaultComponentTsGenerator.DefaultComponentTsGenerator())
        #generators.append(DefaultModuleTsGenerator.DefaultModuleTsGenerator())
        return generators

    def build(self):

        AppModuleTsGenerator.AppModuleTsGenerator().build()
        AppComponentTsGenerator.AppComponentTsGenerator().build()
        AppRoutingModuleTsGenerator.AppRoutingModuleTsGenerator().build()
        generators = self.getGenerators()
        for entity in Entity.select():
            for generator in generators:
                new_entity = aliasEntity.AliasEntity(entity.table, entity.name, entity.keyColumn, entity.namePortuguese, entity.shortName)
                generator.setEntity(new_entity)
                generator.build()

        self.finishApi()
        return

    def PoBuild(self):

        generators = self.getPoGenerators()
        for entity in Entity.select():
            for generator in generators:
                new_entity = aliasEntity.AliasEntity(entity.table, entity.name, entity.keyColumn, entity.namePortuguese, entity.shortName)
                generator.setEntity(new_entity)
                generator.build()
        return

    def PoStart(self):
        
        # print('Instalando Angular')
        # os.system('npm uninstall -g @angular/cli')
        # os.system('npm cache clean --force')
        # os.system('npm i -g @angular/cli')

        # print('\nInstalando o projeto my-po-project')
        # os.system('ng new my-po-project --skipInstall --interactive=false')

        print('\nDependencias do package.json corrigidas.')
        PackageJson = PackageJsonGenerator.PackageJsonGenerator()
        PackageJson.setFileOut()
        PackageJson.build()

        print('\nInstalando dependencias')
        os.system('cd '+ settings.PATH_PO +' & npm install')

        print('\nAdiconando o pacote @portinari/portinari-ui')
        os.system('cd '+ settings.PATH_PO +' & ng add @portinari/portinari-ui --defaults=true')

        print('\nInicializando o projeto')
        os.system('cd '+ settings.PATH_PO +' & ng serve -o --liveReload=true')

        return
    
    def PoServe(self):
        print('\nInicializando o projeto')
        os.system('cd '+ settings.PATH_PO +' & ng serve -o')

    def finishApi(self):
        ApiCodeGen = ApiCodeGenerator.ApiCodeGenerator()
        ApiCodeGen.finishApi()
