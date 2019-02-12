import pymssql, settings

class ManagementDb:

    #gera uma conexão com o banco
    def conn(self):
        conn = pymssql.connect(
            server=settings.DATABASES['default']['HOST'], 
            user=settings.DATABASES['default']['USER'], 
            password=settings.DATABASES['default']['PASSWORD'], 
            database=settings.DATABASES['default']['NAME']
        )
        return conn    
    
    #Testa uma conexão com o banco executando uma query simples
    def testeConnect(self):
        
        conn = self.conn()
        cursor = conn.cursor()

        cursor.execute("SELECT 1 ")
        row = cursor.fetchone()
        cursor.close()

        if row[0] == 1:
            print("Connection " + settings.DATABASES['default']['NAME'] + " OK! ")
        else:
            print("Connection " + settings.DATABASES['default']['NAME'] + " Fail! =( ")

        return

    #Retorna o tipo da coluna no banco de dados
    def getColumnInfo(self, table, column):

        conn = self.conn()

        query = (
                    " SELECT " 
                    " COLUMN_NAME, " 
                    " DATA_TYPE, " 
                    " CHARACTER_MAXIMUM_LENGTH " 
                    " FROM INFORMATION_SCHEMA.COLUMNS " 
                    " WHERE " 
                    " TABLE_NAME = '" + table + "' "  
                )

        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        return result



