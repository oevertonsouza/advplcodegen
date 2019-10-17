import peewee
 
database = peewee.SqliteDatabase("advplcodegen.db")

def CreateTables():
    try:
        Entity.create_table()
    except peewee.OperationalError:
        print ("Entity table already exists!")

    try:
        Colunas.create_table()
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
    variabelName = peewee.CharField()
    options = peewee.CharField()
 
    class Meta:
        database = database
 
if __name__ == "__main__":
    CreateTables()