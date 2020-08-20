# -*- coding: utf-8 -*-
import sys
import pymssql
import settings

class ManagementDb:

    #gera uma conexao com o banco
    def conn(self):
        conn = pymssql.connect(
            server=settings.DATABASES['default']['HOST'], 
            user=settings.DATABASES['default']['USER'], 
            password=settings.DATABASES['default']['PASSWORD'], 
            database=settings.DATABASES['default']['NAME']
        )
        return conn    

    #Testa uma conexao com o banco executando uma query simples
    def testeConnect(self):
        
        conn = self.conn()
        cursor = conn.cursor()

        tableName = "B3K"


        cursor.execute("SELECT 1 ")
        row = cursor.fetchone()
        cursor.close()

        if row[0] == 1:
            print("Connection " + settings.DATABASES['default']['NAME'] + " OK! ")
        else:
            print("Connection " + settings.DATABASES['default']['NAME'] + " Fail! =( ")
        return

    #Retorna o tipo da coluna no banco de dados
    def getColumnDesc(self, tableName):

        conn = self.conn()

        query = (
                    " SELECT X3_CAMPO "
                    "     ,X3_TITENG  "
                    "     ,X3_DESCENG "
                    "     ,X3_TIPO "
                    "     ,X3_TAMANHO "
                    "     ,X3_DECIMAL "
                    "     ,X3_CBOX "
                    "     ,X3_DESCRIC "
                    " FROM SX3" + settings.PROTHEUS_ENVIORMENT['default']['COMPANY'] + "0 "
                    " WHERE 1=1 "
                    "   AND X3_ARQUIVO = '"+ tableName[:3] +"' "
                    "   AND X3_CAMPO  <> '"+ tableName[:3] +'_FILIAL'+ "' "
                    "   AND D_E_L_E_T_ = ' '"
                    "   AND X3_CONTEXT <> 'V'" #N�o pega campos virtuais
                    "   AND X3_CONTEXT <> ''"  
                    " ORDER BY X3_ORDEM"
                )

        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        return result
    #Retorna os dados da tabela do SX2
    def getTableInfo(self, tableName):

        conn = self.conn()
        query = (
                    " SELECT X2_NOMEENG, X2_NOME, X2_UNICO "
                    " FROM SX2" + settings.PROTHEUS_ENVIORMENT['default']['COMPANY'] + "0 "
                    " WHERE 1=1 "
                    "   AND X2_CHAVE = '"+ tableName[:3] +"' "
                    "   AND D_E_L_E_T_ = ' '")
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()

        return result