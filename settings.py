# -*- coding: cp1252 -*-
import os

#DataBase Info
DATABASES = {
    'default': {
        'NAME': 'P12125MNTDB',
        'USER': 'sa',
        'PASSWORD': 'masterkey',
        'HOST': 'localhost',
    }
}

#Protheus Info
PROTHEUS_ENVIORMENT = {
    'default': {
        'COMPANY' : 'T1',
        'FILIAL' : '01',
        'PREFIX' : 'Cen',
        'SEGMENT' : 'healthcare' ,
        'PRODUCT' : 'Central de Obrigacoes',
        'PRDUCT_DESCRIPTION' : 'Central de Obrigacoes',
        'DICTIONARY_IN_DATABASE' : True,
        'CONTACT' : 'comiteintegracao@totvs.com.br',
    }
}

PATH_PROJECT = os.path.dirname(os.path.abspath(__file__))

#Project Path
PATH_SRC = os.path.join(PATH_PROJECT, "src")
PATH_TEMPLATE = os.path.join(PATH_PROJECT, "templates")
PATH_TEMP = os.path.join(PATH_PROJECT, "temp")
PATH_FILESTORAGE = os.path.join(PATH_PROJECT, "filestorage")
PATH_DATABASE = os.path.join(PATH_PROJECT, "sqliteadmin")
PATH_PO = os.path.join(PATH_PROJECT, "my-po-project")
PATH_PO_SRC = os.path.join(PATH_PO, "src")
PATH_DATABASE = os.path.join(PATH_PROJECT, "sqliteadmin")


#Inside portinari
PATH_PO_SRC_ENVIRONMENTS = os.path.join(PATH_PO_SRC, "environments")
PATH_PO_SRC_APP = os.path.join(PATH_PO_SRC, "app")
PATH_PO_SRC_APP_SHARED = os.path.join(PATH_PO_SRC_APP, "shared")

#Inside src
PATH_SRC_API = os.path.join(PATH_SRC, "api")
PATH_SRC_DAO = os.path.join(PATH_SRC, "dao")
PATH_SRC_COLLECTION = os.path.join(PATH_SRC, "collection")
PATH_SRC_ENTITY = os.path.join(PATH_SRC, "entity")
PATH_SRC_LIB = os.path.join(PATH_SRC, "lib")
PATH_SRC_DOC = os.path.join(PATH_SRC, "doc")
PATH_SRC_DOC_API = os.path.join(PATH_SRC_DOC, "apis")
PATH_SRC_DOC_SCHEMA = os.path.join(PATH_SRC_DOC, "schemas")
PATH_SRC_TEST = os.path.join(PATH_SRC, "test")
PATH_SRC_MAPPER = os.path.join(PATH_SRC, "mapper")
PATH_SRC_REQUEST = os.path.join(PATH_SRC, "request")
PATH_SRC_COMMAND = os.path.join(PATH_SRC, "command")
PATH_SRC_VALIDATE = os.path.join(PATH_SRC, "validate")


#Inside Template
PATH_TEMPLATE_LIBS = os.path.join(PATH_TEMPLATE, "libs")
PATH_TEMPLATE_DOCS = os.path.join(PATH_TEMPLATE, "docs")
PATH_TEMPLATE_PO = os.path.join(PATH_TEMPLATE, "portinari")
PATH_TEMPLATE_PO_SHARED = os.path.join(PATH_TEMPLATE_PO, "shared")
PATH_TEMPLATE_PO_ENTITY = os.path.join(PATH_TEMPLATE_PO, "entity")
PATH_TEMPLATE_PO_ENTITY_FORM = os.path.join(PATH_TEMPLATE_PO_ENTITY, "entity-form")
PATH_TEMPLATE_PO_ENTITY_LIST = os.path.join(PATH_TEMPLATE_PO_ENTITY, "entity-list")
PATH_TEMPLATE_PO_ENTITY_VIEW = os.path.join(PATH_TEMPLATE_PO_ENTITY, "entity-view")
PATH_TEMPLATE_PO_ENVIRONMENTS = os.path.join(PATH_TEMPLATE_PO, "environments")

#Inside Test
PATH_SRC_TEST_CASES = os.path.join(PATH_SRC_TEST, "cases")
PATH_SRC_TEST_GROUP = os.path.join(PATH_SRC_TEST, "group")
PATH_SRC_TEST_SUITE = os.path.join(PATH_SRC_TEST, "suite")

