#include "TOTVS.CH"

Class Mapper

    Data oEntity
    Data nType

    Method New() Constructor
    Method getEntity()
    Method setEntity(oEntity)
    Method getType()
    Method setType(nType)

EndClass

Method New(oEntity) Class Mapper
    self:oEntity := oEntity
Return self

Method getEntity() Class Mapper
Return self:oEntity

Method setEntity(oEntity) Class Mapper
    self:oEntity := oEntity
Return

Method getType() Class Mapper
Return self:nType

Method setType(nType) Class Mapper
    self:nType := nType
Return
