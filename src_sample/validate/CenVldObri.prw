#INCLUDE "PROTHEUS.CH"
#INCLUDE "TOTVS.CH"

Class CenVldObri from CenVldDIOPS

    Method New() Constructor
    Method validate(oEntity)

EndClass

Method New() Class CenVldObri
    _Super:New()
Return self

Method validate(oEntity) Class CenVldObri
Return _Super:validate(oEntity)
