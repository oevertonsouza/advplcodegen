#INCLUDE "TOTVS.CH"

#Define DBFIELD 1
#Define JSONFIELD 2

Class CenDaoObri from CenDao

    Method New(aFields) Constructor

    Method buscar()
    Method insert()
    Method commit()
    Method delete()    
    Method bscChaPrim()
    
EndClass

Method New(aFields) Class CenDaoObri
	_Super:New(aFields)
    self:cAlias := "B3A"
    self:cfieldOrder := "B3A_CODIGO,B3A_CODOPE,B3A_FILIAL"
Return self

Method buscar() Class CenDaoObri
	Local lFound := .F.
    lFound := _Super:buscar()
    If lFound 
		B3A->(DbGoto((self:getAliasTemp())->RECNO))
    EndIf
Return lFound

Method delete() Class CenDaoObri
    Local lFound := .F.
	if self:bscChaPrim()
        lFound := _Super:delete()    
    EndIf
Return lFound

Method bscChaPrim() Class CenDaoObri

    Local lFound := .F.
	Local cQuery := ""

    cQuery := " SELECT "
    cQuery += _Super:getFields()
    cQuery += " FROM " + RetSqlName('B3A') + " "
	cQuery += " WHERE 1=1 "
	cQuery += " AND	B3A_FILIAL = '" + xFilial("B3A") + "' "

    cQuery += " AND B3A_CODIGO = ? "
    aAdd(self:aMapBuilder, self:toString(self:getValue("obligationCode")))
    cQuery += " AND B3A_CODOPE = ? "
    aAdd(self:aMapBuilder, self:toString(self:getValue("providerRegister")))
    cQuery += " AND B3A_FILIAL = ? "
    aAdd(self:aMapBuilder, self:toString(self:getValue("systemBranch")))

    cQuery += " AND D_E_L_E_T_ = ? "
    aAdd(self:aMapBuilder, ' ')
    self:setQuery(self:queryBuilder(cQuery))
	lFound := self:executaQuery()

return lFound

Method insert() Class CenDaoObri
    Local lFound := !self:bscChaPrim()
	If lFound
        self:commit(.T.)
    EndIf
Return lFound

Method commit(lInclui) Class CenDaoObri

    Default lInclui := .F.

	If B3A->(RecLock("B3A",lInclui))
		
        B3A->B3A_FILIAL := xFilial("B3A")
        If lInclui
        
            B3A->B3A_CODIGO := _Super:normalizeType(B3A->B3A_CODIGO,self:getValue("obligationCode")) /* Column B3A_CODIGO */
            B3A->B3A_CODOPE := _Super:normalizeType(B3A->B3A_CODOPE,self:getValue("providerRegister")) /* Column B3A_CODOPE */
            B3A->B3A_FILIAL := _Super:normalizeType(B3A->B3A_FILIAL,self:getValue("systemBranch")) /* Column B3A_FILIAL */

        EndIf

        B3A->B3A_SZNLDD := _Super:normalizeType(B3A->B3A_SZNLDD,self:getValue("seasonality")) /* Column B3A_SZNLDD */
        B3A->B3A_TIPO := _Super:normalizeType(B3A->B3A_TIPO,self:getValue("obligationType")) /* Column B3A_TIPO */
        B3A->B3A_DESCRI := _Super:normalizeType(B3A->B3A_DESCRI,self:getValue("obligationDescription")) /* Column B3A_DESCRI */
        B3A->B3A_ATIVO := _Super:normalizeType(B3A->B3A_ATIVO,self:getValue("activeInactive")) /* Column B3A_ATIVO */
        B3A->B3A_AVVCTO := _Super:normalizeType(B3A->B3A_AVVCTO,self:getValue("dueDateNotification")) /* Column B3A_AVVCTO */

        B3A->(MsUnlock())
        lFound := .T.
    EndIf
Return lFound
