# -*- coding: utf-8 -*-
import csv
import os
import re
import sys
from pathlib import Path

from advplcodegen import settings
from advplcodegen.core.codeGenerators import (
                ApiCodeGenerator, CollectionCodeGenerator,
                CommandCodeGenerator, DaoCodeGenerator, DocApiCodeGenerator,
                DocApiSchemaCodeGenerator, MapperCodeGenerator,
                RequestCodeGenerator, TestCaseCodeGenerator,
                TestGroupCodeGenerator, TestSuiteCodeGenerator,
                ValidateCodeGenerator, entityCodeGenerator
            )
from advplcodegen.core.codeGenerators.portinari import (
                AppComponentTsGenerator,AppRoutingModuleTsGenerator,
                DefaultComponentHtmlGenerator
            )
from advplcodegen.core import storage


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
                    for generator in generators:  
                        generator.setEntity(entity[0])
                        generator.setName(entity[1])
                        generator.setShortName(entity[3])
                        generator.setNamePortuguese(entity[4])
                        generator.build()
        return

    def finishApi(self):
        ApiCodeGen = ApiCodeGenerator.ApiCodeGenerator()
        ApiCodeGen.finishApi()
