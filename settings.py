# -*- coding: cp1252 -*-
import os

#DataBase Info
DATABASES = {
    'default': {
        'NAME': 'NAME',
        'USER': 'USER',
        'PASSWORD': 'PASSWORD',
        'HOST': 'HOST',
    }
}

#Protheus Info
PROTHEUS_ENVIORMENT = {
    'default': {
        'COMPANY' : 'COMPANY',
        'FILIAL' : 'FILIAL',
        'PREFIX' : 'PREFIX',
        'SEGMENT' : 'SEGMENT  
        'PRODUCT' : 'PRODUCT',
        'PRDUCT_DESCRIPTION' : 'PRDUCT_DESCRIPTION',
        'DICTIONARY_IN_DATABASE' : True,
        'CONTACT' : 'CONTACT',
    }
}

PATH_PROJECT = os.path.dirname(os.path.abspath(__file__))

#Project Path
PATH_SRC = os.path.join(PATH_PROJECT, "src")
PATH_TEMPLATE = os.path.join(PATH_PROJECT, "templates")
PATH_TEMP = os.path.join(PATH_PROJECT, "temp")
PATH_FILESTORAGE = os.path.join(PATH_PROJECT, "filestorage")

#Inside src
PATH_SRC_API = os.path.join(PATH_SRC, "api")
PATH_SRC_DAO = os.path.join(PATH_SRC, "dao")
PATH_SRC_COLLECTION = os.path.join(PATH_SRC, "collection")
PATH_SRC_ENTITY = os.path.join(PATH_SRC, "entity")
PATH_SRC_LIB = os.path.join(PATH_SRC, "lib")
PATH_SRC_DOC = os.path.join(PATH_SRC, "doc")
PATH_SRC_TEST = os.path.join(PATH_SRC, "test")
PATH_SRC_MAPPER = os.path.join(PATH_SRC, "mapper")
PATH_SRC_REQUEST = os.path.join(PATH_SRC, "request")
PATH_SRC_COMMAND = os.path.join(PATH_SRC, "command")
PATH_SRC_VALIDATE = os.path.join(PATH_SRC, "validate")

#Inside Template
PATH_TEMPLATE_LIBS = os.path.join(PATH_TEMPLATE, "libs")
PATH_TEMPLATE_DOCS = os.path.join(PATH_TEMPLATE, "docs")

#Inside Test
PATH_SRC_TEST_CASES = os.path.join(PATH_SRC_TEST, "cases")
PATH_SRC_TEST_GROUP = os.path.join(PATH_SRC_TEST, "group")
PATH_SRC_TEST_SUITE = os.path.join(PATH_SRC_TEST, "suite")