#include "TOTVS.CH"

#DEFINE CARACTER "C"
#DEFINE NUMBER "N"
#DEFINE BOOLEAN "L"
#DEFINE DATE "D"
#DEFINE ARRAY "A"
#DEFINE OBJECT "O"

Class EntityAbstract

    Data hMap
    Data oFields
	
    Method New()
    Method hasValue(cProperty,cType)
    Method getValue(cProperty)
    Method setValue(cProperty,anyValue)
    Method getFields()

EndClass

Method New() Class EntityAbstract
	self:hMap := THashMap():New()
Return self

Method hasValue(cProperty,cType) Class EntityAbstract

    Local anyValue := ""
    default cType := CARACTER

    lFound := self:hMap:get(cProperty,@anyValue)
    lFound := !empty(anyValue)
	
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

Method getValue(cProperty) Class EntityAbstract
	Local anyValue := ""
	self:hMap:get(cProperty,@anyValue)
Return anyValue

Method setValue(cProperty,anyValue) Class EntityAbstract
	self:hMap:set(cProperty,@anyValue)
Return 

Method getFields() Class EntityAbstract
	self:oFields := HMList():New()
	self:initFields()
Return self:oFields
