# -*- coding: utf-8 -*-
import sys, os, csv, re
import settings
from core import managedb
from pathlib import Path
import peewee
from core.daos.model import Entity, Column

class Storage:

    def __init__(
                self
            ):
        return

    #Gera as colunas no arquivo .storage, para usar no build
    def genColumnStorage(self, entity):
        mdb = managedb.ManagementDb()
        
        tableInfo = mdb.getTableInfo(entity.table)
        uniqueColumns = tableInfo[0][2].strip().split('+')
        columnList = mdb.getColumnDesc(entity.table)
       
        for field in columnList:
            dbField = field[0]
            is_indice = dbField in uniqueColumns
            is_keyPathParam = dbField == entity.keyColumn 
            name = re.sub('[^A-Za-z0-9]+', '', field[2].title())
            name = name[0].lower() + name[1:]
            desc = field[7].strip()
            opcoes = field[6].strip().replace(";",",")
            length = str(field[4])
            if field[3] == 'C':
                dataType = "string"
            elif field[3] == 'D':
                dataType = "date"
            elif field[3] == 'N':
                dataType = "float"
                length = str(int(field[4]))
            else:  
                dataType = "string"
            varName = field[3].lower() + re.sub('[^A-Za-z0-9]+', '', field[1].title())
            
            
            new_column = Column.create( entity = entity,
                                dbField = dbField,
                                name = name,
                                dataType = dataType,
                                length = length,
                                is_indice = is_indice,
                                is_keyPathParam = is_keyPathParam,
                                desc = desc,
                                variabelName = varName,
                                options = opcoes)

        return
 