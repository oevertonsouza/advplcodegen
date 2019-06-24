# -*- coding: utf-8 -*-
import sys, os, settings, csv, re
from core import managedb
from pathlib import Path

class Storage:

    def __init__(
                self
            ):
        return

    #Gera as colunas no arquivo .storage, para usar no build
    def genColumnStorage(self, entity, keyParam):
        columnList = []
        f = open(os.path.join(settings.PATH_FILESTORAGE , entity + ".columns"), "w+")
        mdb = managedb.ManagementDb()
        columnInfo = mdb.getColumnInfo(entity)
        if settings.PROTHEUS_ENVIORMENT['default']['DICTIONARY_IN_DATABASE']:
            columnList = mdb.getColumnDesc(entity)
        is_indice = ''
        dataType = ''
        is_keyPathParam = ''
    
        for column in columnInfo:
            name = column[0].replace("_", "").lower()
            length = str(column[2])
            is_indice = "1" if column[3] == 2 else "0"
            is_keyPathParam = "1" if column[0] == keyParam else "0"
            dataType = "string" if column[1] == "varchar" else column[1]
            desc = 'Descricao do campo'
            opcoes = ""
            for field in columnList:
                if column[0].strip() in field[0]:
                    name = re.sub('[^A-Za-z0-9]+', '', field[2].title())
                    name = name[0].lower() + name[1:]
                    desc = field[7].strip()
                    opcoes = field[6].strip().replace(";",",")
                    if field[3] == 'C':
                        dataType = "string"
                    elif field[3] == 'D':
                        dataType = "date"
                    elif field[3] == 'N':
                        dataType = "float"
                        length = str(int(field[4]))
            
            f.write( column[0]+';'+name+';'+dataType+';'+length+';'+is_indice+';'+is_keyPathParam+';'+desc+";"+opcoes+';\n')
        
        f.close()
    
        return
