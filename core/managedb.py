# -*- coding: utf-8 -*-
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
    def getColumnInfo(self, entity):

        conn = self.conn()

        query = (
                    "   SELECT  "
                    "   	COLUMN_NAME,    "
                    "   	DATA_TYPE,  "
                    "   	CHARACTER_MAXIMUM_LENGTH,   "
                    "   	INDEX_NUM = COUNT(*)    "
                    "   FROM    "
                    "   (   "
                    "   SELECT  "
                    "   	sf.COLUMN_NAME, "
                    "   	sf.DATA_TYPE,   "
                    "   	sf.CHARACTER_MAXIMUM_LENGTH "
                    "   FROM    "
                    "        sys.indexes ind    "
                    "   INNER JOIN  "
                    "        sys.index_columns ic ON  ind.object_id = ic.object_id and ind.index_id = ic.index_id   "
                    "   INNER JOIN  "
                    "        sys.columns col ON ic.object_id = col.object_id and ic.column_id = col.column_id   "
                    "   INNER JOIN  "
                    "        sys.tables t ON ind.object_id = t.object_id    "
                    "   LEFT JOIN   "
                    "        INFORMATION_SCHEMA.COLUMNS sf ON sf.COLUMN_NAME = col.name "
                    "   WHERE   "
                    "       ind.is_primary_key = 0  "
                    "       AND ind.is_unique = 0   "
                    "       AND ind.is_unique_constraint = 0    "
                    "       AND t.is_ms_shipped = 0     "
                    "   	AND ind.name= '" + entity + "1' "
                    "   group by    "
                    "   	sf.COLUMN_NAME, "
                    "   	sf.DATA_TYPE,   "
                    "   	sf.CHARACTER_MAXIMUM_LENGTH "
                    "   UNION ALL   "
                    "   SELECT      "
                    "   	COLUMN_NAME,    "
                    "   	DATA_TYPE,  "
                    "   	CHARACTER_MAXIMUM_LENGTH    "
                    "   FROM INFORMATION_SCHEMA.COLUMNS     "
                    "   WHERE   "
                    "   TABLE_NAME = '" + entity + "'   "
                    "   ) INFO  "
                    "   where   "
                    "   	COLUMN_NAME not in ('R_E_C_N_O_', 'D_E_L_E_T_','R_E_C_D_E_L_','" + entity[:3] + "_FILIAL')"
                    "   group by    "
                    "   	COLUMN_NAME,    "
                    "   	DATA_TYPE,  "
                    "   	CHARACTER_MAXIMUM_LENGTH    "
                    "   ORDER BY    "
                    "   	INDEX_NUM desc  "
                )

        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        return result
    #Retorna o tipo da coluna no banco de dados
    def getColumnDesc(self, entity):

        conn = self.conn()

        query = (
                    " SELECT X3_CAMPO,X3_TITENG "
                    "     ,X3_DESCENG "
                    "     ,X3_TIPO "
                    "     ,X3_CBOX "
                    " FROM SX3" + entity[3:] + " "
                    " WHERE 1=1 "
                    "   AND X3_ARQUIVO = '"+ entity[:3] +"' "
                    "   AND D_E_L_E_T_ = ' '"
                    " ORDER BY X3_ORDEM"
                )

        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        return result