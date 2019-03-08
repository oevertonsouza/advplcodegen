#include "TOTVS.CH"

/*/{Protheus.doc} Collection
    Classe abstrata de uma Coleção de registros de uma entifade.
    Esta classe deve orquestrar as operações feitas em coleções de registros. 
    Isso envolve:
        - Buscas de registros específicos
        - Buscas de coleções de registros
        - Iterações sobre cada registro retornado
        - Deleção ou atualização de coleções de registros

    @type  Class
    @author everton.mateus
    @since 20190222
/*/
Class Collection
	   
    Data oDao
    Data oMapper
    Data hMap
    Data lFound
    Data listKeys
    Data listValues
    Data nIndex
    Data nRecno
    Data lIndexed
    Data nOper
    Data cCustomWhere
    Data cError
    Data lFault

    Method New() Constructor
    Method destroy()
    Method found()
    Method connectionFault()
    Method setError(cMsg)
    Method getFault()
    Method hasNext()
    Method getNext()
    Method setIndex(nIndex)
    Method addKeyValue(xValue)
    Method addCustomIdx(cKey, xValue)
    Method seekByIndex()
    Method isFilterBy(cKeyFilter)
    Method goTop()
    Method applyPageSize(cPage,cPageSize)
    Method getDao()
    Method getQuery()
    Method applyOrder(cOrder)
    Method setValue(cProperty,xData)
    Method getValue(cProperty)
    Method fillIndex()
    Method buscar()
        
EndClass

Method New() Class Collection
    self:lFound := .F.
    self:lIndexed := .F.
    self:lFault := .F.
    self:listKeys := HMList():New()
    self:listValues := HMList():New()
    self:cError := ""
    self:hMap := THashMap():New()
return self


Method destroy() Class Collection

    if !empty(self:getDao())
        self:getDao():destroy()
        FreeObj(self:oDao)
        self:oDao := nil
    endif

    if !empty(self:oMapper)
        FreeObj(self:oMapper)
        self:oMapper := nil
    endif
    
    if !empty(self:hMap)
        FreeObj(self:hMap)
        self:hMap := nil
    endif

return

Method found() Class Collection
    if !self:lFound .And. !empty(self:getDao():getError())
        self:setError(self:getDao():getError())
    endif
return self:lFound

Method connectionFault() Class Collection
return self:lFault

Method setError(cMsg) Class Collection
    self:cError := cMsg
    self:lFault := .T.
return

Method getFault() Class Collection
return self:cError

Method hasNext() Class Collection
return self:getDao():hasNext(self:nRecno)

Method getNext() Class Collection
    self:oMapper:setEntity(self:initEntity())
    self:oMapper:mapFromDao(self:getDao())
    self:nRecno++
return self:oMapper:getEntity()

Method setIndex(nIndex) Class Collection
    self:nIndex := nIndex
return

Method addKeyValue(xValue) Class Collection
    self:listValues:push(xValue)
return

Method addCustomIdx(cKey, xValue) Class Collection
    self:listKeys:push(cKey)
    self:listValues:push(xValue)
return

Method seekByIndex() Class Collection
    self:fillIndex()

	self:listKeys:goTop()
	self:listValues:goTop()
    
    self:lFound := self:getDao():seekByIndex(self:listKeys,self:listValues)
    self:nRecno := 1

return self:found()

Method isFilterBy(cKeyFilter) Class Collection

    Local lIsFiltering := .F.
    Local nControl     := 0
    Local cKey         := ""
    Local xValue       := ""

    self:listKeys:goTop()
    self:listValues:goTop()
    while !lIsFiltering .and. cKey <> cKeyFilter .and. self:listKeys:hasNext() .and. nControl < self:listValues:size()
        cKey := self:listKeys:getNext()
        xValue := self:listValues:getNext()
        lIsFiltering := (lower(cKey) == lower(cKeyFilter) .and. !empty(xValue))
        nControl++
    endDo

return {lIsFiltering, xValue}

Method goTop() Class Collection
    self:nRecno := 1
    self:getDao():posReg(self:nRecno)
return

Method applyPageSize(cPage,cPageSize) Class Collection

    self:getDao():setNumPage(cPage)
    self:getDao():setPageSize(cPageSize)

return

Method getDao() Class Collection
Return self:oDao

Method getQuery() Class Collection
Return self:getDao():getQuery()

Method applyOrder(cOrder) Class Collection
    self:getDao():setOrder(cOrder)
return

Method setValue(cProperty,xData) Class Collection
    self:getDao():setValue(cProperty,xData)
Return self:hMap:set(cProperty,xData)

Method getValue(cProperty) Class Collection
	Local anyValue := ""
	self:hMap:get(cProperty,@anyValue)
Return anyValue

Method fillIndex() Class Collection
Return

Method buscar() Class Collection
    self:lFound := self:getDao():buscar()
    self:goTop()
Return self:found()