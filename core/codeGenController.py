# -*- coding: utf-8 -*-
import csv
import os
import re
import sys
from pathlib import Path

import settings
from core.codeGenerators import (
                ApiCodeGenerator, CollectionCodeGenerator,
                CommandCodeGenerator, DaoCodeGenerator, DocApiCodeGenerator,
                DocApiSchemaCodeGenerator, MapperCodeGenerator,
                RequestCodeGenerator, TestCaseCodeGenerator,
                TestGroupCodeGenerator, TestSuiteCodeGenerator,
                ValidateCodeGenerator, entityCodeGenerator
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
        generators.append(AppComponentTsGenerator.AppComponentTsGenerator())
        generators.append(AppRoutingModuleTsGenerator.AppRoutingModuleTsGenerator())
        generators.append(DefaultComponentHtmlGenerator.DefaultComponentHtmlGenerator())
        generators.append(DefaultComponentTsGenerator.DefaultComponentTsGenerator())
        generators.append(AppModuleTsGenerator.AppModuleTsGenerator())
        #generators.append(DefaultModuleTsGenerator.DefaultModuleTsGenerator())
        return generators

    def build(self):

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  "storage.entity")
        exists = os.path.isfile(storagePathFile) 

        if exists:
            generators = self.getGenerators()
            with open(storagePathFile) as datafile:
                data = csv.reader(datafile, delimiter=';')
                for entity in data:
                    if len(entity) > 0:
                        for generator in generators:
                            generator.setEntity(entity[0])
                            generator.setName(entity[1])
                            generator.setShortName(entity[3])
                            generator.setNamePortuguese(entity[4])
                            generator.build()

            self.finishApi()
        return

    def PoBuild(self):

        storagePathFile = os.path.join(settings.PATH_FILESTORAGE ,  "storage.entity")
        exists = os.path.isfile(storagePathFile) 

        if exists:
            generators = self.getPoGenerators()
            with open(storagePathFile) as datafile:
                data = csv.reader(datafile, delimiter=';')
                for entity in data:
                    if len(entity) > 0:
                        for generator in generators:
                            generator.setEntity(entity[0])
                            generator.setName(entity[1])
                            generator.setShortName(entity[3])
                            generator.setNamePortuguese(entity[4])
                            generator.build()
        return

    def PoStart(self):
        
        #print('Instalando Angular')
        #os.system('npm uninstall -g @angular/cli')
        #os.system('npm cache clean --force')
        #os.system('npm i -g @angular/cli')

        print('\nInstalando o projeto my-po-project')
        os.system('ng new my-po-project --skipInstall --interactive=false')

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
