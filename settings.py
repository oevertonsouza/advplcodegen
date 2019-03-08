import os

DATABASES = {
    'default': {
        'NAME': 'NAME',
        'USER': 'USER',
        'PASSWORD': 'PASSWORD',
        'HOST': 'HOST',
    }
}

PATH_PROJECT = os.path.dirname(os.path.abspath(__file__))
PATH_SRC = os.path.join(PATH_PROJECT, "src")
PATH_TEMPLATE = os.path.join(PATH_PROJECT, "templates")
PATH_FILESTORAGE = os.path.join(PATH_PROJECT, "filestorage")

#Inside API Path
PATH_SRC_API = os.path.join(PATH_SRC, "api")
PATH_SRC_DAO = os.path.join(PATH_SRC, "dao")
PATH_SRC_COLLECTION = os.path.join(PATH_SRC, "collection")
PATH_SRC_ENTITY = os.path.join(PATH_SRC, "entity")
PATH_SRC_LIB = os.path.join(PATH_SRC, "lib")
PATH_SRC_DOC = os.path.join(PATH_SRC, "doc")

#libs Dir
PATH_TEMPLATE_LIBS = os.path.join(PATH_TEMPLATE, "libs")