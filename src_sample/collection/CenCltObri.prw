#include "TOTVS.CH"

Class CenCltObri from CenCollection
	   
    Method New() Constructor
    Method initEntity()

EndClass

Method New() Class CenCltObri
    _Super:new()
    self:oMapper := CenMprObri():New()
    self:oDao := CenDaoObri():New(self:oMapper:getFields())
return self

Method initEntity() Class CenCltObri
return CenObri():New()
