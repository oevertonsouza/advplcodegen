#include "TOTVS.CH"

Class Entity 

    Data hMap
    Data oFields
	
    Method New()
    Method hasValue(cProperty,cType)
    Method getValue(cProperty)
    Method setValue(cProperty,anyValue)
    Method getFields()

EndClass

Method New() Class Entity
	self:hMap := THashMap():New()
Return self

Method hasValue(cProperty,cType) Class Entity
    Local anyValue := ""
    default cType := CARACTER

    lFound := self:hMap:get(cProperty,@anyValue)
    lFound := !(empty(anyValue))
	
	if !lFound
        DO CASE
            CASE cType == CARACTER
                self:hMap:set(cProperty,"")
            CASE cType == NUMBER
                self:hMap:set(cProperty,0)
            CASE cType == BOOLEAN
                self:hMap:set(cProperty,.F.)
            CASE cType == DATE
                self:hMap:set(cProperty,StoD(""))
            CASE cType == ARRAY
                self:hMap:set(cProperty,{})
            CASE cType == OBJECT
                self:hMap:set(cProperty,nil)
	    END CASE
    endIf

Return lFound

Method getValue(cProperty) Class Entity
	Local anyValue := ""
	self:hMap:get(cProperty,@anyValue)
Return anyValue

Method setValue(cProperty,anyValue) Class Entity
	self:hMap:set(cProperty,@anyValue)
Return 

Method getFields() Class Entity
	self:oFields := HMList():New()
	self:initFields()
Return self:oFields
