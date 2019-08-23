#INCLUDE "PROTHEUS.CH"
#INCLUDE "TOTVS.CH"
#INCLUDE "RESTFUL.CH"

#DEFINE SINGLE "01"
#DEFINE ALL    "02"
#DEFINE INSERT "03"
#DEFINE DELETE "04"
#DEFINE UPDATE "05"
#DEFINE BUSCA  "07"

Class CenReqObri from CenRequest

    Method New(oRest,cSvcName) Constructor
    Method destroy()
    Method applyFilter(nType)
    Method applyOrder(cOrder)
    Method buscar(nType)
    Method prepFilter()

EndClass

Method destroy()  Class CenReqObri
Return _Super:destroy()

Method New(oRest, cSvcName) Class CenReqObri
    _Super:New(oRest,cSvcName)
    self:oCollection := CenCltObri():New()
    self:oValidador := CenVldObri():New()
    self:cPropLote   := "Obri"
Return self

Method applyFilter(nType) Class CenReqObri
    
    If self:lSuccess
        If nType == ALL
            self:oCollection:setValue("obligationCode",self:oRest:obligationCode)
            self:oCollection:setValue("providerRegister",self:oRest:providerRegister)
            self:oCollection:setValue("systemBranch",self:oRest:systemBranch)
            self:oCollection:setValue("seasonality",self:oRest:seasonality)
            self:oCollection:setValue("obligationType",self:oRest:obligationType)
            self:oCollection:setValue("obligationDescription",self:oRest:obligationDescription)
            self:oCollection:setValue("activeInactive",self:oRest:activeInactive)
            self:oCollection:setValue("dueDateNotification",self:oRest:dueDateNotification)

        EndIf
        If nType == SINGLE 
            self:oCollection:setValue("obligationCode",self:oRest:obligationCode)
            self:oCollection:setValue("providerRegister",self:oRest:providerRegister)
            self:oCollection:setValue("systemBranch",self:oRest:systemBranch)

        EndIf
    EndIf
Return self:lSuccess

Method applyOrder(cOrder) Class CenReqObri
    If self:lSuccess
        self:oCollection:applyOrder(cOrder)
    EndIf
Return self:lSuccess

Method prepFilter(oJson) Class CenReqObri

    Default oJson := self:jRequest
    self:oCollection:setValue("obligationCode", self:oRest:obligationCode)
    self:oCollection:setValue("providerRegister", self:oRest:providerRegister)
    self:oCollection:setValue("systemBranch", self:oRest:systemBranch)
    
    self:oCollection:mapFromJson(oJson)

Return

Method buscar(nType) Class CenReqObri

    Local lExiste := .F.
    If self:lSuccess
        If nType == BUSCA
            self:lSuccess := self:oCollection:buscar()
        Else
            lExiste := self:oCollection:bscChaPrim()
            If nType == INSERT
                self:lSuccess := !lExiste
            Else
                self:lSuccess := lExiste
            EndIf
        EndIf
    EndIf

Return self:lSuccess


