#include "TOTVS.CH"
#INCLUDE 'FWMVCDEF.CH'

#DEFINE SINGLE "01"
#DEFINE ALL    "02"
#DEFINE INSERT "03"
#DEFINE DELETE "04"
#DEFINE UPDATE "05"
#DEFINE LOTE "06"

#DEFINE SQLSERVER  "MSSQL"

/*/{Protheus.doc} 
    Classe abstrata que faz o controle de abertura e fechamento e posicionamento de alias
    @type  Class
    @author everton.mateus
    @since 29/11/2017
    @version version
/*/

Class Dao

	Data cQuery
	Data cAlias
	Data cAliasTemp
	Data cCodOpe
	Data cNumPage
	Data cPageSize
	Data cDB
	Data cFields
	Data cfieldOrder
	Data oHashOrder
	Data aMapBuilder
    Data oStatement  
	Data hMap
	Data cError

	Method New() Constructor

	Method destroy()
	Method getQuery()
	Method setValue(cProperty,xData)
	Method getValue(cProperty)
	Method getCodOpe()
	Method setCodOpe(cCodOpe)
	Method setNumPage(cNumPage)
	Method setPageSize(cPageSize)
	Method getNumPage()
	Method getPageSize()
	Method getRowControl()
	Method getWhereRow()
	Method getQryPage()
	Method setQuery(cQuery)
	Method getAliasTemp()
	Method aliasSelected()
	Method executaQuery()
	Method execStatement()
	Method getQtd()
	Method fechaQuery()
	Method verificaPos(nRecno)
	Method getTypeOpe(lExiste, nType)
	Method posReg(nRecno)
	Method posDbRecno(nRecno)
	Method setOrder(cOrder)
	Method queryBuilder(cQuery)
	Method buscar()
	Method bscRecno()
	Method delete()
	Method getFields()
	Method getFilters()
	Method seekByIndex(listKeys, listValues)
	Method FilterByKey(listKeys, listValues)
	Method getError()
	Method toString(xValue)
	Method hasNext()

EndClass

Method New() Class Dao
	self:cDB := TcGetDB()
	self:oHashOrder := THashMap():New()
	self:aMapBuilder := {}
    self:oStatement :=  FWPreparedStatement():New()
    self:cNumPage 	:=  "1"
    self:cPageSize 	:=  "0"
	self:hMap := THashMap():New()
Return self

Method destroy() Class Dao
	self:fechaQuery()
Return

Method getQuery() Class Dao
Return self:cQuery

Method setValue(cProperty,xData) Class Dao
Return self:hMap:set(cProperty,xData)

Method getValue(cProperty) Class Dao
	Local anyValue := ""
	self:hMap:get(cProperty,@anyValue)
Return anyValue

Method getCodOpe() Class Dao
	if empty(self:cCodOpe)
		self:setCodOpe("0001")
	endIf
Return self:cCodOpe

Method setCodOpe(cCodOpe) Class Dao
	self:cCodOpe := cCodOpe
Return

Method setNumPage(cNumPage) Class Dao
    self:cNumPage := cNumPage 
Return

Method setPageSize(cPageSize) Class Dao
    self:cPageSize := cPageSize
Return

Method getNumPage() Class Dao
Return self:cNumPage

Method getPageSize() Class Dao
Return self:cPageSize

Method getRowControl() Class Dao

	Local cQuery := ""
	
	// Para fazer o controle da paginação em SQL, usado dessa maneira porque OFFSET e FETCH não funciona em versões sql menor que 2012
	If SQLSERVER $ self:cDB
		cQuery += " WITH " + self:cAlias + " AS ( SELECT ROW_NUMBER() OVER(ORDER BY " + self:cfieldOrder + " ) AS ROW#, "
	Else
		cQuery += " SELECT "
	EndIf

Return cQuery

Method getWhereRow() Class Dao

	Local cQuery := ""
	Local cNumIni := alltrim(str((val(self:cNumPage ) - 1) * val(self:cPageSize)))
	Local cNumFim := alltrim(str(((val(self:cNumPage )) * val(self:cPageSize)) + 1))

	// Para fazer o controle da paginação em SQL, usado dessa maneira porque OFFSET e FETCH não funciona em versões sql menor que 2012
	If SQLSERVER $ self:cDB  
		cQuery += " ) SELECT * FROM " + self:cAlias
		If val(self:cPageSize) > 0
			cQuery += " WHERE ROW# > " + cNumIni 
			cQuery += "  AND ROW# <= " + cNumFim
		EndIf
	EndIf

Return cQuery

Method getQryPage() Class Dao

    Local cQuery := ""
    Local cNumPage := alltrim(str((val(self:cNumPage ) - 1) * val(self:cPageSize)))

    //Nesse ponto, pegamos sempre 1 registro a mais do tamanho da página para efeitos de paginação na tela.
    cQuery += " OFFSET " + cNumPage + " ROWS FETCH NEXT " + SOMA1(self:cPageSize) + " ROWS ONLY "

Return cQuery

Method setQuery(cQuery) Class Dao
	self:cQuery := cQuery
Return

Method getAliasTemp() Class Dao
	if empty(self:cAliasTemp)
		self:cAliasTemp := getNextAlias()
	endif
Return self:cAliasTemp

Method aliasSelected() Class Dao
Return Select(self:getAliasTemp()) > 0

Method executaQuery() Class Dao
	Local lFound := .F.

	self:fechaQuery()
	self:setQuery(self:getQuery())
	dbUseArea(.T.,"TOPCONN",TCGENQRY(,,self:getQuery()),self:getAliasTemp(),.F.,.T.)
	/*	
		Essa linha serve para conferirmos se todos os alias abertos foram fechados.
		Nos codereviews devemos: Descomentar, compilar, fechar o server, apagar o appserver.log, 
		abrir o server, rodar o autorizadortestsuite, abrir o appserver.log e 
		conferir se o total de :abriu == total de :fechou
	*/
	//conout(self:getAliasTemp()+":abriu:"+procName(6)+">"+procName(5)+">"+procName(4)+">"+procName(3)+">"+procName(2)+">"+procName(1)+": "+self:getQuery()) 
	lFound := (self:getAliasTemp())->(!Eof())
	If !lFound
		self:fechaQuery()
	EndIf
	
Return lFound

Method execStatement() Class Dao
	Local lSuccess := .F.

	lSuccess := TcSqlExec(self:getQuery()) >= 0
	If lSuccess .AND. SubStr(Alltrim(Upper(TCGetDb())),1,6) == "ORACLE"
		lSuccess := TCSQLEXEC("COMMIT") >= 0
	Endif

	If !lSuccess
		self:cError := TcSqlError()
	EndIf
	
Return lSuccess

Method getQtd() Class Dao
Return (self:getAliasTemp())->QTD

Method fechaQuery() Class Dao
	if self:aliasSelected()
		(self:getAliasTemp())->(dbCloseArea())
		/*	
			Essa linha serve para conferirmos se todos os alias abertos foram fechados.
			Nos codereviews devemos: Descomentar, compilar, fechar o server, apagar o appserver.log, 
			abrir o server, rodar o autorizadortestsuite, abrir o appserver.log e conferir se o total de :abriu == total de :fechou
		*/
		//conout(self:getAliasTemp()+":fechou:"+procName(6)+">"+procName(5)+">"+procName(4)+">"+procName(3)+">"+procName(2)+">"+procName(1)+": "+self:getQuery()) 
	endIf
Return

Method verificaPos(nRecno) Class Dao

	If  self:aliasSelected() .and. nRecno != (self:getAliasTemp())->(RECNO())
		self:posReg(nRecno)
	EndIf

Return

Method getTypeOpe(lExiste, nType) Class Dao

	Local nOperation := nil

	If (!lExiste .AND. nType == INSERT .OR. nType == LOTE)
        nOperation := MODEL_OPERATION_INSERT
    ElseIf (lExiste .AND. nType == DELETE)
        nOperation := MODEL_OPERATION_DELETE
    ElseIf (lExiste .AND. nType != INSERT .AND. nType != DELETE ) 
        nOperation := MODEL_OPERATION_UPDATE
    EndIf

Return nOperation

Method posReg(nRecno) Class Dao
	Local nSkip := 0
	If self:aliasSelected() 
		If nRecno < (self:getAliasTemp())->(RECNO())
			(self:getAliasTemp())->(dbGoTop())
			If nRecno <> 1
				nSkip := nRecno-1
			EndIf
		Else
			nSkip := nRecno-(self:getAliasTemp())->(RECNO())
		EndIf
		If nRecno <> 1
			(self:getAliasTemp())->(dbSkip(nSkip))
		EndIf
		self:posDbRecno((self:getAliasTemp())->RECNO)
	EndIf
Return

Method posDbRecno(nRecno) Class Dao
	Local lFound := .F.
	If nRecno <> (self:cAlias)->(RECNO())
		(self:cAlias)->(DbGoto(nRecno))
	EndIf
Return !(self:cAlias)->(Eof())

Method setOrder(cOrder) Class Dao
	Local aOrder 
	Local cDesc
	Local nI 	 	 := 0
	Local cField 	 := ""
	Local cTypeOrder := " ASC "

	aOrder = StrTokArr(cOrder, "," )

	If !Empty(cOrder)
		
		For nI := 1 to Len( aOrder )
		
			cField := UPPER(aOrder[nI])
			cDesc = SubStr(cField,1,1)

			If cDesc == "-"
				cField := SubStr(cField, 2, LEN(cField))
				cTypeOrder := " DESC "
			EndIf

			If self:oHashOrder:get(cField)

				self:oHashOrder:get(cField, cField)

				If nI = 1
					self:cfieldOrder := " " + cField + cTypeOrder
				Else
					self:cfieldOrder += " , " + cField + cTypeOrder
				EndIf

			EndIf
		Next nI
	EndIf
Return

Method queryBuilder(cQuery) Class Dao

    Local nStatement := 1
    Local cQryFixed := ""

    self:oStatement:SetQuery(cQuery) 
    
    For nStatement:= 1 to Len(self:aMapBuilder)
        self:oStatement:SetString( nStatement , self:aMapBuilder[nStatement])
    Next

    cQryFixed := self:oStatement:GetFixQuery()

    self:aMapBuilder := nil
    self:aMapBuilder := {}

    self:oStatement := nil 
    self:oStatement :=  FWPreparedStatement():New()

Return cQryFixed

Method buscar() Class Dao
	
    Local cQuery := ""
	Local lFound := .F.

    cQuery += " SELECT "    
    cQuery += self:getFields()
    cQuery += " FROM " + RetSqlName(self:cAlias) + " " + self:cAlias + " "
    cQuery += self:getFilters()

    cQuery := self:queryBuilder(cQuery)

    self:setQuery(cQuery)
    lFound := self:executaQuery()

Return lFound

Method delete() Class Dao
    Local cQuery := ""
    Local lFound := .F.

    cQuery := " DELETE FROM "
    cQuery += " " + RetSqlName(self:cAlias) + " "
    cQuery += " WHERE "
    cQuery += self:getFilters()
    cQuery := self:queryBuilder(cQuery)
    self:setQuery(cQuery)
    lFound := self:execStatement()

Return lFound

Method getFields() Class Dao
	Local cFilter
	cFilter += " " + self:cAlias + "_FILIAL = '" + xFilial(self:cAlias) + "' "
    xValue := self:getValue("recno")
    if !empty(xValue)
        cFilter += " AND R_E_C_N_O_ =  ? "
        aAdd(self:aMapBuilder, self:toString(xValue))
    EndIf
    cFilter += " AND D_E_L_E_T_ = ? "
    aAdd(self:aMapBuilder, ' ')

	 
Return self:cFields

Method getFilters() Class Dao

    Local cQuery := ""

    cQuery += " "+ self:cAlias + "_FILIAL = '" + xFilial( self:cAlias ) + "' "
    cQuery += " AND " + self:cAlias + ".D_E_L_E_T_ 	= ? "
    aAdd(self:aMapBuilder, ' ')

Return cQuery

Method seekByIndex(listKeys, listValues) Class Dao
    
    Local cQuery := ""
    Local lFound := .F.

    cQuery += " SELECT "    
    cQuery += self:getFields()
    cQuery += " FROM " + RetSqlName(self:cAlias) + " " + self:cAlias + " "
    cQuery += self:filterByKey(listKeys, listValues)
    cQuery := self:queryBuilder(cQuery)

    self:setQuery(cQuery)
    lFound := self:executaQuery()
 
Return lFound 

Method FilterByKey(listKeys, listValues) Class Dao
    Local cFilters := " WHERE "
    
    cFilters += " " + self:cAlias + "_FILIAL = '" + xFilial(self:cAlias) + "' "

	while listKeys:hasNext()
        cFilters += " AND " + listKeys:getNext() + " = ? "
        aAdd(self:aMapBuilder, listValues:getNext())
    enddo

    cFilters += " AND " + self:cAlias + ".D_E_L_E_T_ 	= ? "
    aAdd(self:aMapBuilder, ' ')

Return cFilters

Method getError() Class Dao
Return ""

Method toString(xValue) Class Dao
	Local cValue := ""

	If xValue == Nil
		cValue := ""
	ElseIf ValType( xValue ) == "N"
		cValue := AllTrim(Str(xValue))
	ElseIf ValType( xValue ) == "C"
		cValue := xValue
	ElseIf ValType( xValue ) == "D"
		cValue := DTOS(xValue)
	EndIf

Return cValue

Method hasNext(nRecno) Class Dao
    Local lTemProx := .F.
    If self:aliasSelected()
        self:verificaPos(nRecno)
        lTemProx := !(self:getAliasTemp())->(Eof())
    EndIf
return lTemProx