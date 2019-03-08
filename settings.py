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
PATH_API = os.path.join(PATH_PROJECT, "api")
PATH_TEMPLATE = os.path.join(PATH_PROJECT, "templates")
PATH_FILESTORAGE = os.path.join(PATH_PROJECT, "filestorage")

#Inside API Path
PATH_API_DAO = os.path.join(PATH_API, "dao")
PATH_API_COLLECTION = os.path.join(PATH_API, "collection")
PATH_API_ENTITY = os.path.join(PATH_API, "entity")
PATH_API_LIB = os.path.join(PATH_API, "lib")
PATH_API_DOC = os.path.join(PATH_API, "doc")

#libs Dir
PATH_TEMPLATE_LIBS = os.path.join(PATH_TEMPLATE, "libs")