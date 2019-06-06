# -*- coding: utf-8 -*-
import sys, os, settings, csv, re
from core import managedb, commandController, apiController, codeGenerator
from pathlib import Path

class Storage:

    def __init__(
                self
            ):
        return

    #Gera as colunas no arquivo .storage, para usar no build
    def genColumnStorage(self, entity, keyParam):
        
        f = open(os.path.join(settings.PATH_FILESTORAGE , entity + ".columns"), "w+")
        mdb = managedb.ManagementDb()
        columnInfo = mdb.getColumnInfo(entity)
        columnList = mdb.getColumnDesc(entity)
        is_indice = ''
        dataType = ''
        is_keyPathParam = ''
    
        for column in columnInfo:
            desc = column[0].replace("_", "").lower()
            for field in columnList:
                if column[0].strip() in field[0]:
                    desc = re.sub('[^A-Za-z0-9]+', '', field[2])
                    desc = desc[0].lower() + desc[1:]
                    
            if column[3] == 2:
                is_indice = "1"
            else:
                is_indice = "0"
            
            if column[1] == "varchar":
                dataType = "string"
            else:
                dataType = column[1]
            
            if column[0] == keyParam:
                is_keyPathParam = "1"
            else:
                is_keyPathParam = "0"
            
            f.write( column[0]+';'+desc+';'+dataType+';'+str(column[2])+';'+is_indice+';'+is_keyPathParam+'\n')
        
        f.close()
    
        return
