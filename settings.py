import os

DATABASES = {
    'default': {
        'NAME': 'P12Atual',
        'USER': 'sa',
        'PASSWORD': 'masterkey',
        'HOST': '10.171.67.105',
    }
}

PATH_PROJECT = os.path.dirname(os.path.abspath(__file__))
PATH_API = os.path.join(PATH_PROJECT, "api")
PATH_TEMPLATE = os.path.join(PATH_PROJECT, "templates")
PATH_FILESTORAGE = os.path.join(PATH_PROJECT, "filestorage")

#Inside API Path
PATH_API_DAO = os.path.join(PATH_API, "dao")
PATH_API_SEEKER = os.path.join(PATH_API, "seeker")
PATH_API_ENTITY = os.path.join(PATH_API, "entity")
PATH_API_LIB = os.path.join(PATH_API, "lib")

#Inside Template Path
PATH_TEMPLATE_ENTITY = os.path.join(PATH_TEMPLATE, "entity")

