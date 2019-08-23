#include "TOTVS.CH"

#Define DBFIELD 1
#Define JSONFIELD 2

/*/{Protheus.doc} 
    Classe abstrata de um CenMapper
    @type  Class
    @author victor.silva
    @since 20180718
/*/
Class CenMapper

    Data oEntity
    Data nType
    Data aFields

    Method New() Constructor
    Method getEntity()
    Method setEntity(oEntity)
    Method mapFromDao(oDao) 
    Method mapFromJson(oJson)
    Method getFields()

EndClass

Method New(oEntity) Class CenMapper
    self:oEntity := oEntity
    self:aFields := {}
Return self

Method getEntity() Class CenMapper
Return self:oEntity

Method setEntity(oEntity) Class CenMapper
    self:oEntity := oEntity
Return

Method mapFromDao(oDao) Class CenMapper
    Local nField := 0
    Local nLen   := Len(self:aFields)
    Local xValue := ""

    For nField := 1 to nLen
        xValue := (oDao:cAliasTemp)->&(self:aFields[nField][DBFIELD])
        If ValType( xValue ) == "C"
            xValue := AllTrim(xValue)
        EndIf
        self:oEntity:setValue(self:aFields[nField][JSONFIELD],xValue )
    Next nField
Return

Method mapFromJson(oJson) Class CenMapper
    Local nField := 0
    Local nLen   := Len(self:aFields)

    For nField := 1 to nLen
        cField := self:aFields[nField][JSONFIELD]
        self:oEntity:setValue(cField,oJson[cField])
    Next nField
    
Return self:getEntity()

Method getFields() Class CenMapper
Return self:aFields