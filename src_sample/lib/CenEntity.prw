#include "TOTVS.CH"
//#include "autorizador.ch"

/*/{Protheus.doc} 
    Classe abstrata de uma entidade de negócio
    @type  Class
    @author 
    @since 
/*/
Class CenEntity 

    Data hMap
    Data cJson
    Data nRecno
    Data oHashFields
	
	Method New() Constructor
	
	Method getHMap()
	Method setHMap(hMap)
	Method setValue(cProperty,xData)
	Method destroy()
	Method getValue(cProperty)
	Method dateToUtc(dDate, cTime, utc)
	Method utcToDate(cUtcDate)
	Method setHashFields(oHashFields)

EndClass

Method New() Class CenEntity
	self:hMap 		:= THashMap():New()
	self:nRecno 	:= 1
Return self

Method getHMap() Class CenEntity
Return self:hMap

Method setHMap(hMap) Class CenEntity
	self:hMap := hMap
Return

Method setValue(cProperty,xData) Class CenEntity
Return self:hMap:set(cProperty,xData)

Method destroy() Class CenEntity
	if !empty(self:hMap)
        self:hMap:clean()
        FreeObj(self:hMap)
        self:hMap := nil
    endif
	if !empty(self:oHashFields)
        self:oHashFields:clean()
        FreeObj(self:oHashFields)
        self:oHashFields := nil
    endif
return

Method getValue(cProperty) Class CenEntity
	Local anyValue := ""
	self:hMap:get(cProperty,@anyValue)
Return anyValue

Method dateToUtc(dDate, cTime, utc) Class CenEntity

	Local cUtcDate := ""
	Local dVoidDate := STOD("")

	If dDate != dVoidDate
		If utc 
			cUtcDate := allTrim(FWTimeStamp(5, dDate, cTime))  
		else
			cUtcDate := SubStr(allTrim(FWTimeStamp(5, dDate, cTime)), 1, 10)
		EndIF
	EndIf

Return cUtcDate

Method utcToDate(cUtcDate) Class CenEntity
	
	Local dDate := STOD("")

	If !Empty(cUtcDate)
		dDate := STOD(SubStr(allTrim(STRTRAN(cUtcDate, "-", "")), 1, 8))
	EndIF

Return dDate

//Armazena os fields para serializar a saida Json do Objeto
Method setHashFields(oHashFields) Class CenEntity
    self:oHashFields := oHashFields
Return