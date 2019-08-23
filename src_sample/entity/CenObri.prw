#include "TOTVS.CH"

/*/{Protheus.doc} 
    Classe concreta da Entidade CenObri - Obligations
    @type  Class
    @author FrameworkApi 1.0
    @since 20190211
/*/
Class CenObri from CenEntity

    Method New()
  
    Method serialize(oJsonControl)
    Method destroy()

EndClass

Method New() Class CenObri
	_Super:New()
Return self

Method serialize(oJsonControl) Class CenObri

	local oJson := JsonObject():New()
	default oJsonControl := CenJsonControl():New()

    oJsonControl:setProp(oJson,"obligationCode",self:getValue("obligationCode")) /* Column B3A_CODIGO */ 
    oJsonControl:setProp(oJson,"providerRegister",self:getValue("providerRegister")) /* Column B3A_CODOPE */ 
    oJsonControl:setProp(oJson,"systemBranch",self:getValue("systemBranch")) /* Column B3A_FILIAL */ 
    oJsonControl:setProp(oJson,"seasonality",self:getValue("seasonality")) /* Column B3A_SZNLDD */ 
    oJsonControl:setProp(oJson,"obligationType",self:getValue("obligationType")) /* Column B3A_TIPO */ 
    oJsonControl:setProp(oJson,"obligationDescription",self:getValue("obligationDescription")) /* Column B3A_DESCRI */ 
    oJsonControl:setProp(oJson,"activeInactive",self:getValue("activeInactive")) /* Column B3A_ATIVO */ 
    oJsonControl:setProp(oJson,"dueDateNotification",self:getValue("dueDateNotification")) /* Column B3A_AVVCTO */ 

Return oJson

Method destroy() Class CenObri
	_Super:destroy()
	DelClassIntF()
return