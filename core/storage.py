# -*- coding: utf-8 -*-
import sys, os, settings, csv
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
        is_indice = ''
        dataType = ''
        is_keyPathParam = ''
    
        for column in columnInfo:
            
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
            

            keyParam
            
            f.write( column[0]+';'+column[0].replace("_", "").lower()+';'+dataType+';'+str(column[2])+';'+is_indice+';'+is_keyPathParam+'\n')
        
        f.close()
    
        return
