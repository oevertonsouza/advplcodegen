#include "TOTVS.CH"
#INCLUDE 'FWMVCDEF.CH'

/*/{Protheus.doc} 
    Collection
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

Class CenCollection
	   
    Data oDao
    Data oMapper
    Data hMap
    Data lFound
    Data nRecno
    Data cError
    Data lFault

    Method New() Constructor
    Method destroy()
    Method found()
    Method setError(cMsg)
    Method getError()
    Method hasNext()
    Method getNext()
    Method mapFromJson(cJson)
    Method goTop()
    Method applyPageSize(cPage,cPageSize)
    Method getPageSize()
    Method getDao()
    Method getQuery()
    Method applyOrder(cOrder)
    Method setValue(cProperty,xData)
    Method getValue(cProperty)
    Method commit()
    Method insert()
    Method update()
    Method delete()
    Method buscar()
    Method bscChaPrim()
    Method setEntity(oEntity)

EndClass

Method New() Class CenCollection
    self:lFound := .F.
    self:lFault := .F.
    self:cError := ""
    self:hMap := THashMap():New()
return self


Method destroy() Class CenCollection

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
        self:hMap:clean()
        FreeObj(self:hMap)
        self:hMap := nil
    endif

return

Method found() Class CenCollection
return self:lFound

Method setError(cMsg) Class CenCollection
    self:cError := cMsg
    self:lFault := .T.
return

Method getError() Class CenCollection
return self:cError

Method hasNext() Class CenCollection
return self:getDao():hasNext(self:nRecno)

Method getNext() Class CenCollection
    self:oMapper:setEntity(self:initEntity())
    self:oMapper:mapFromDao(self:getDao())
    self:nRecno++
return self:oMapper:getEntity()

Method mapFromJson(oJson) Class CenCollection
    self:oMapper:setEntity(self)
    self:oMapper:mapFromJson(oJson)
return self:oMapper:getEntity()

Method goTop() Class CenCollection
    self:nRecno := 1
    self:getDao():posReg(self:nRecno)
return

Method applyPageSize(cPage,cPageSize) Class CenCollection
    self:getDao():setNumPage(cPage)
    self:getDao():setPageSize(cPageSize)
return

Method getPageSize() Class CenCollection
return self:getDao():getPageSize()

Method getDao() Class CenCollection
Return self:oDao

Method getQuery() Class CenCollection
Return self:getDao():getQuery()

Method applyOrder(cOrder) Class CenCollection
    self:getDao():setOrder(cOrder)
return

Method setValue(cProperty,xData) Class CenCollection
    self:getDao():setValue(cProperty,xData)
Return self:hMap:set(cProperty,xData)

Method getValue(cProperty) Class CenCollection
	Local anyValue := ""
	self:hMap:get(cProperty,@anyValue)
Return anyValue

Method commit() Class CenCollection
    self:lFound := self:getDao():commit()
    If !self:found()
        self:setError("Não conseguiu incluir o registro. " + self:getDao():getError() )
    EndIf
Return self:found()

Method insert() Class CenCollection
    self:lFound := self:getDao():insert()
    If !self:found()
        self:setError("Não conseguiu incluir o registro. " + self:getDao():getError() )
    EndIf
Return self:found()

Method update() Class CenCollection
Return self:commit()

Method delete() Class CenCollection
    self:lFound := self:getDao():delete()
    If !self:found()
        self:setError("Não conseguiu deletar o registro. " + self:getDao():getError())
    EndIf
Return self:found()

Method buscar() Class CenCollection
    self:lFound := self:getDao():buscar()
    self:goTop()
Return self:found()

Method bscChaPrim() Class CenCollection
    self:lFound := self:getDao():bscChaPrim()
    self:goTop()
Return self:found()

Method setEntity(oEntity) Class CenCollection
    self:oMapper:setEntity(oEntity)
    self:oDao:setHMap(oEntity:getHMap())
return
