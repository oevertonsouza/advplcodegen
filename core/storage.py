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
    def genColumnStorage(self, entity):
        
        f = open(os.path.join(settings.PATH_FILESTORAGE , entity + ".columns"), "w+")
        mdb = managedb.ManagementDb()
        columnInfo = mdb.getColumnInfo(entity)
        is_indice = ''
        dataType = ''
    
        for column in columnInfo:
            if column[3] == 2:
                is_indice = "1"
            else:
                is_indice = "0"
            if column[1] == "varchar":
                dataType = "string"
            else:
                dataType = column[1]
            
            f.write( column[0]+';'+column[0].replace("_", "").lower()+';'+dataType+';'+str(column[2])+';'+is_indice+';0\n')
        
        f.close()
    
        return
