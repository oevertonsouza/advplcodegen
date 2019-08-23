#include "TOTVS.CH"
#include 'FWMVCDEF.CH'

/*/ CenJsonControl
Encapsula objeto da TEC JsonObject para controlar os filtros

@type   class
@author victor.silva
@since  20180523
/*/

Class CenJsonControl

    Data hmFields
    Data hmExpand
    Data lFiltered
    Data lExpanding
    
    Method New()
    
    Method prepFields(cFields)
    
    Method notFiltered()
    Method fillArray(oJson,cProp,oValue)
    Method newArray(oJson,cProp)
    Method newObj(oJson,cProp)
    Method printProp(cProp)
    Method setProp(oJson,cProp,cValue)
    Method setPropObj(oJson,cObj,cProp,cValue)
    Method addObjtoProp(oJson,cProp, oObj)

EndClass

Method New() Class CenJsonControl
    self:lFiltered     := .F.
    self:lExpanding    := .F.
    self:hmFields      := THashMap():New()
    self:hmExpand      := THashMap():New()
Return self

Method prepFields(cFields) Class CenJsonControl
    Local aFields     := {}
    Local nFields     := 1
    Local nLenFields  := 0

    if !empty(cFields)
        self:lFiltered := .T.
        aFields := StrTokArr2(cFields, ",")
        nLenFields := Len(aFields)
        self:hmFields:set("nLenFields",nLenFields)
        for nFields := 1 to nLenFields
            self:hmFields:set(aFields[nFields],aFields[nFields])
        next nFields
    endif
    
return

Method notFiltered() Class CenJsonControl
Return !self:lFiltered .Or. self:lExpanding

Method fillArray(oJson,cProp,oValue) Class CenJsonControl
    
    if !empty(oValue)
        aAdd(oJson[cProp],oValue:serialize(self))
    else
        aAdd(oJson[cProp],JsonObject():New())
    endif
return

Method addObjtoProp(oJson,cProp, oObj) Class CenJsonControl
    
    if !empty(oObj:toJson())
        aAdd(oJson[cProp], oObj)
    else
        aAdd(oJson[cProp],JsonObject():New())
    endif

return

Method newArray(oJson,cProp) Class CenJsonControl
    oJson[cProp] := {}
return

Method newObj(oJson,cProp) Class CenJsonControl
    oJson[cProp] := JsonObject():New()
return

Method printProp(cProp) Class CenJsonControl
return !self:lFiltered .Or. (self:lFiltered .And. self:hmFields:get(cProp))

Method setProp(oJson,cProp,cValue) Class CenJsonControl
    if self:printProp(cProp) .Or. self:lExpanding
        oJson[cProp] := cValue
    endif
return

Method setPropObj(oJson,cObj,cProp,cValue) Class CenJsonControl
    if self:printProp(cProp) .Or. self:lExpanding
        oJson[cObj][cProp] := cValue
    endif
return
