#INCLUDE "TOTVS.CH"

Class RestRequest

    Data oRest
    Data nRequest
    Data cResponse
    Data lSuccess
    Data nStatus
    Data nFault
    Data cFaultDesc
    Data cFaultDetail
    Data oReqBody
    Data oRespBody
    Data oRespControl
    Data nMediaType
    Data cMsgId

    Method New(oRest, nRequest)
    Method initRequest()
    Method setMediaType(nMediaType)
    Method applyFields()
    Method applyExpandables()
    Method endRequest()
    Method getRestResult()

EndClass

Method New(oRest, nRequest) Class RestRequest
    self:oRest        := oRest
    self:nRequest     := nRequest
    self:lSuccess     := .T.
    self:nStatus      := 200
    self:oReqBody     := JsonObject():New()
    self:oRespBody    := JsonObject():New()
    self:oRespControl := AutJsonControl():New()
    self:nFault       := 0
    self:cFaultDesc   := ''
    self:cResponse    := ''
    self:cFaultDetail := ''
    self:cMsgId       := FWUUIDV4(.T.)
Return self

Method initRequest() Class RestRequest
Return

Method setMediaType(nMediaType) Class RestRequest
    self:nMediaType := nMediaType
Return self:lSuccess

Method applyFields() Class RestRequest
    self:oRespControl:prepFields(self:oRest:fields)
Return

Method applyExpandables() Class RestRequest
    if self:lSuccess
        self:oRespControl:prepExpand(self:oRest:expand)
    endif
Return

Method endRequest() Class RestRequest
    Local cResponse := ""
    
    if self:lSuccess
        self:oRest:setStatus(self:nStatus,"")
        cResponse := EncodeUTF8(self:cResponse)
        self:oRest:setResponse(cResponse)
    else
        self:oRest:setStatus(self:nStatus,"")
        cResponse := EncodeUTF8(self:serializeFault())
        self:oRest:setResponse(cResponse)
    endif

Return self:lSuccess

Method getRestResult() Class RestFacade
Return .T.
