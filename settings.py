import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'P12Atual',
        'USER': 'sa',
        'PASSWORD': 'masterkey',
        'HOST': '10.171.67.105',
    }
}

PATH_PROJECT = os.path.dirname(os.path.abspath(__file__))

