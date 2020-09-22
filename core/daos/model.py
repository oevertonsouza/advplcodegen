import peewee
import settings
import os

database = peewee.SqliteDatabase(os.path.join(settings.PATH_DATABASE,"advplcodegen.db"))

def CreateTables():
    try:
        Entity.create_table()
    except peewee.OperationalError:
        print ("Entity table already exists!")

    try:
        Colunas.create_table()
    except peewee.OperationalError:
        print ("Columns table already exists!")
    
    try:
        Relations.create_table()
    except peewee.OperationalError:
        print ("Columns table already exists!")
    
    try:
        RelationKeys.create_table()
    except peewee.OperationalError:
        print ("Columns table already exists!")

########################################################################
class Entity(peewee.Model):
    
    name = peewee.CharField(unique=True)
    table = peewee.CharField(unique=True)
    shortName = peewee.CharField()
    namePortuguese = peewee.CharField()
    keyColumn = peewee.CharField()
    
    class Meta:
        database = database

########################################################################
class Relations(peewee.Model):
            
    table = peewee.CharField(unique=True)
    tableRelation = peewee.CharField(unique=True)
    relationType = peewee.CharField()
    behavior = peewee.CharField()
  
    class Meta:
        database = database

########################################################################
class RelationKeys(peewee.Model):

    relation = peewee.ForeignKeyField(Relations)

    column = peewee.CharField(unique=True)
    columnRelation = peewee.CharField()
    
    class Meta:
        database = database

########################################################################
class Colunas(peewee.Model):

    entity = peewee.ForeignKeyField(Entity)

    dbField = peewee.CharField(unique=True)
    name = peewee.CharField()
    dataType = peewee.CharField()
    length = peewee.IntegerField()
    is_indice = peewee.BooleanField()
    is_keyPathParam = peewee.BooleanField()
    is_required = peewee.BooleanField()
    desc = peewee.CharField()
    variablename = peewee.CharField()
    options = peewee.CharField()
 
    class Meta:
        database = database
 
if __name__ == "__main__":
    CreateTables()

