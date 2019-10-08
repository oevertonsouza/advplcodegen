# -*- coding: cp1252 -*-
import sys, os, settings, csv, shutil
import settings
from core.codeGenerators.codeGenerator import codeGenerator
from string import Template

class PackageJsonGenerator(codeGenerator):

    def __init__ (self, entity=None):
        super().__init__(entity=None)
        self.templateFile = 'package.json.template'
        self.templatePath = settings.PATH_TEMPLATE_PO
        self.srcPath = settings.PATH_PO
        return

    def setFileOut(self):
        self.fileOut = "package.json"
    
    def getVariables(self):
        dependencies = (
            '  "dependencies": {'
            '    "@angular/animations": "~8.0.0",'
            '    "@angular/common": "~8.0.0",'
            '    "@angular/compiler": "~8.2.2",'
            '    "@angular/core": "~8.0.0",'
            '    "@angular/forms": "~8.0.0",'
            '    "@angular/platform-browser": "~8.0.0",'
            '    "@angular/platform-browser-dynamic": "~8.0.0",'
            '    "@angular/platform-server": "~8.0.0",'
            '    "@angular/router": "~8.0.0",'
            '    "rxjs": "~6.4.0",'
            '    "zone.js": "~0.9.1"'
            '  },'
            '  "devDependencies": {'
            '    "@angular-devkit/build-angular": "~0.803.5",'
            '    "@angular/cli": "~8.3.6",'
            '    "@angular/compiler-cli": "~8.2.7",'
            '    "@angular/language-service": "~8.2.7",'
            '    "@types/node": "~8.9.4",'
            '    "@types/jasmine": "~3.3.8",'
            '    "@types/jasminewd2": "~2.0.3",'
            '    "codelyzer": "^5.0.0",'
            '    "jasmine-core": "~3.4.0",'
            '    "jasmine-spec-reporter": "~4.2.1",'
            '    "karma": "~4.1.0",'
            '    "karma-chrome-launcher": "~2.2.0",'
            '    "karma-coverage-istanbul-reporter": "~2.0.1",'
            '    "karma-jasmine": "~2.0.1",'
            '    "karma-jasmine-html-reporter": "^1.4.0",'
            '    "protractor": "~5.4.0",'
            '    "ts-node": "~7.0.0",'
            '    "tslint": "~5.15.0",'
            '    "typescript": "~3.5.3"'
            '  }'
        )

        variables = {
                'dependencies': dependencies, 
            }
        return variables

    def build(self):
        self.writeFile(self.getVariables(''))
        return
