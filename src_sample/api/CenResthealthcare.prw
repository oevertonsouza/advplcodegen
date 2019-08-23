#INCLUDE "TOTVS.CH"
#INCLUDE "RESTFUL.CH"

#DEFINE SINGLE "01"
#DEFINE ALL    "02"
#DEFINE BUSCA  "07"

WSRESTFUL healthcare DESCRIPTION "Exemplo de serviço REST"

    // Atributos padrao utilizados em todas ou em mais de uma solicitacao
    WSDATA apiVersion as STRING  OPTIONAL
    WSDATA page as STRING  OPTIONAL
    WSDATA pageSize as STRING  OPTIONAL
    WSDATA tokenId as STRING  OPTIONAL
    WSDATA action as STRING  OPTIONAL
    WSDATA fields as STRING  OPTIONAL
    WSDATA expand as STRING  OPTIONAL
    WSDATA order as STRING  OPTIONAL
    WSDATA version as STRING  OPTIONAL
    // Propriedades da entidade B3AT10 - Obligations

    WSDATA obligationCode as STRING  OPTIONAL
    WSDATA providerRegister as STRING  OPTIONAL
    WSDATA systemBranch as STRING  OPTIONAL
    WSDATA seasonality as STRING  OPTIONAL
    WSDATA obligationType as STRING  OPTIONAL
    WSDATA obligationDescription as STRING  OPTIONAL
    WSDATA activeInactive as STRING  OPTIONAL
    WSDATA dueDateNotification as STRING  OPTIONAL

    
    // Metodos da entidade B3AT10 - Obligations
    WSMETHOD GET ObriCollection DESCRIPTION "Obligations - Get Collection" ;
    WSsyntax "{version}/obligations" ;
    PATH "{version}/obligations" PRODUCES APPLICATION_JSON

    WSMETHOD GET ObriSingle DESCRIPTION "Obligations - Get Single" ;
    WSsyntax "{version}/obligations/{obligationCode}" ;
    PATH "{version}/obligations/{obligationCode}" PRODUCES APPLICATION_JSON

    WSMETHOD PUT ObriUpdate DESCRIPTION "Obligations - PUT" ;
    WSsyntax "{version}/obligations/{obligationCode}" ;
    PATH "{version}/obligations/{obligationCode}" PRODUCES APPLICATION_JSON

    WSMETHOD POST ObriInsert DESCRIPTION "Obligations - Post" ;
    WSsyntax "{version}/obligations" ;
    PATH "{version}/obligations" PRODUCES APPLICATION_JSON

    WSMETHOD DELETE ObriDelete DESCRIPTION "Obligations - Delete" ;
    WSsyntax "{version}/obligations/{obligationCode}" ;
    PATH "{version}/obligations/{obligationCode}" PRODUCES APPLICATION_JSON

END WSRESTFUL

WSMETHOD GET ObriCollection QUERYPARAM page, pageSize, fields, order,;
    obligationCode,;
    providerRegister,;
    systemBranch,;
    seasonality,;
    obligationType,;
    obligationDescription,;
    activeInactive,;
    dueDateNotification;
    WSSERVICE healthcare

    Local oRequest := CenReqObri():New(self, "obri-get_collection")

    Default self:page     := "1"
    Default self:pageSize := "20"
    Default self:fields   := ""
    Default self:order    := ""

    Default self:obligationCode := ""
    Default self:providerRegister := ""
    Default self:systemBranch := ""

    Default self:seasonality := ""
    Default self:obligationType := ""
    Default self:obligationDescription := ""
    Default self:activeInactive := ""
    Default self:dueDateNotification := ""

    
    oRequest:initRequest()
    if oRequest:checkAuth()
        oRequest:applyFilter(ALL)
        oRequest:applyFields(self:fields)
        oRequest:applyOrder(self:order)
        oRequest:applyPageSize()
        oRequest:buscar(BUSCA)
        oRequest:procGet(ALL)
    endif
    oRequest:endRequest()
    oRequest:destroy()
    oRequest := nil
    DelClassIntf()

Return .T.

WSMETHOD GET ObriSingle PATHPARAM;
    obligationCode;
    QUERYPARAM;
    fields,;    
    providerRegister,;
    systemBranch;
    WSSERVICE healthcare
    
    Local oRequest := CenReqObri():New(self, "obri-get_single")

    Default self:fields   := ""
    
    oRequest:initRequest()
    if oRequest:checkAuth()
        oRequest:applyFilter(SINGLE)
        oRequest:applyFields(self:fields)
        oRequest:applyPageSize()
        oRequest:buscar(BUSCA)
        oRequest:procGet(SINGLE) 
    endif
    oRequest:endRequest()
    oRequest:destroy()
    oRequest := nil
    DelClassIntf()

Return .T.

WSMETHOD PUT ObriUpdate PATHPARAM;
    obligationCode;
    QUERYPARAM;
    providerRegister,;
    systemBranch;
    WSSERVICE healthcare

    Local oRequest := CenReqObri():New(self, "obri-put_update")

    Default self:obligationCode := ""
    Default self:providerRegister := ""
    Default self:systemBranch := ""


    oRequest:initRequest()
    if oRequest:checkAuth()
        oRequest:checkBody()
        oRequest:applyPageSize()
        oRequest:procPut()
    endif

    oRequest:endRequest()
    oRequest:destroy()
    DelClassIntf()

Return .T.

WSMETHOD POST ObriInsert WSSERVICE healthcare

    Local oRequest := CenReqObri():New(self, "obri-post_insert")
   
    Default self:obligationCode := ""
    Default self:providerRegister := ""
    Default self:systemBranch := ""

    Default self:seasonality := ""
    Default self:obligationType := ""
    Default self:obligationDescription := ""
    Default self:activeInactive := ""
    Default self:dueDateNotification := ""


    oRequest:initRequest()
    
    if oRequest:checkAuth()
        oRequest:checkBody()
        oRequest:applyFields(self:fields)
        oRequest:applyPageSize()
        oRequest:procPost()
    endif
    oRequest:endRequest()
    oRequest:destroy()
    DelClassIntf()

Return .T.

WSMETHOD DELETE ObriDelete PATHPARAM;
    obligationCode;
    QUERYPARAM;
    providerRegister,;
    systemBranch;
    WSSERVICE healthcare

    Local oRequest := CenReqObri():New(self, "obri-delete")
    
    oRequest:initRequest()
    if oRequest:checkAuth()
        oRequest:applyFilter(SINGLE)
        oRequest:applyPageSize()        
        oRequest:buscar(SINGLE)
        oRequest:procDelete()
    endif

    oRequest:endRequest()
    oRequest:destroy()
    DelClassIntf()

Return .T.

