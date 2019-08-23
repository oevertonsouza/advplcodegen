#Include 'Protheus.ch'

CLASS CenObriTestCase FROM FWDefaultTestCase
	
	METHOD CenObriTestCase()
	METHOD SetUpClass()
	METHOD TearDownClass()
	METHOD getSingle_001()
	METHOD getCollection_002()
	METHOD insert_003()
	METHOD update_004()
	METHOD delete_005()
	METHOD error_006()

ENDCLASS

METHOD CenObriTestCase() CLASS CenObriTestCase
	_Super:FWDefaultTestCase()
	self:AddTestMethod( "GETSINGLE_001",,"Busca um registro na tabela B3AT10." )
	self:AddTestMethod( "GETCOLLECTION_002",,"Busca uma coleção de registros na tabela B3AT10." )
	self:AddTestMethod( "INSERT_003",,"Insere um registro na tabela B3AT10." )
	self:AddTestMethod( "UPDATE_004",,"Altera um registro na tabela B3AT10." )
	self:AddTestMethod( "DELETE_005",,"Deleta um registro na tabela B3AT10." )
	self:AddTestMethod( "ERROR_006",,"Testa o registro de um erro." )
Return

METHOD SetUpClass() CLASS CenObriTestCase
Return _Super:SetUpClass()

METHOD TearDownClass() CLASS CenObriTestCase
	Local oResult := FWTestHelper():New()

    oResult:UTRestParam(oResult:aParam)
	DelClassIntf()
	
Return oResult

//Test Single Src
METHOD getSingle_001() CLASS CenObriTestCase

	Local oResult := FWTestHelper():New()
	Local aHeader   := {"Content-Type: application/json"}
    Local cRet      := ""
    Local oJson := JsonObject():New()

    Local cCode := "" /*Column B3A_CODIGO*/
    Local cProvReg := "" /*Column B3A_CODOPE*/
    Local cBranch := "" /*Column B3A_FILIAL*/

    Local cSeasonality := "" /*Column B3A_SZNLDD*/
    Local cType := "" /*Column B3A_TIPO*/
    Local cDescription := "" /*Column B3A_DESCRI*/
    Local cActive := "" /*Column B3A_ATIVO*/
    Local nDueDtNotif := 0 /*Column B3A_AVVCTO*/

	oResult:activate()
	oResult:UTSetAPI("/healthcare/v1/obligations/"+escape(cCode)+;
					"?page=1"+;
                    "&providerRegister="+escape(cProvReg)+;
                    "&systemBranch="+escape(cBranch)+;
                    "&order=obligationCode,providerRegister,systemBranch,seasonality,obligationType,obligationDescription,activeInactive,dueDateNotification"+;
                    "&fields=obligationCode,providerRegister,systemBranch,seasonality,obligationType,obligationDescription,activeInactive,dueDateNotification";
                    ,"REST")

	cRet := oResult:UTGetWS(aHeader)
    oResult:AssertFalse(Empty(cRet), "Não houve retorno para a requisição")

	If !Empty(cRet)

        oJson:fromJson(DecodeUTF8(cRet))

        oResult:assertTrue(oJson["obligationCode"] == cCode, "Valor comparado na coluna B3A_CODIGO de alias obligationCode, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["providerRegister"] == cProvReg, "Valor comparado na coluna B3A_CODOPE de alias providerRegister, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["systemBranch"] == cBranch, "Valor comparado na coluna B3A_FILIAL de alias systemBranch, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["seasonality"] == cSeasonality, "Valor comparado na coluna B3A_SZNLDD de alias seasonality, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["obligationType"] == cType, "Valor comparado na coluna B3A_TIPO de alias obligationType, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["obligationDescription"] == cDescription, "Valor comparado na coluna B3A_DESCRI de alias obligationDescription, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["activeInactive"] == cActive, "Valor comparado na coluna B3A_ATIVO de alias activeInactive, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["dueDateNotification"] == nDueDtNotif, "Valor comparado na coluna B3A_AVVCTO de alias dueDateNotification, nao sao iguais. Retorno:" + cRet)  

	EndIf

	oResult:AssertTrue( oResult:lOk, "" )
	oResult:deactivate()

Return oResult

//Test All Src
METHOD getCollection_002() CLASS CenObriTestCase

	Local oResult := FWTestHelper():New()
	Local aHeader   := {"Content-Type: application/json"}
    Local cRet      := ""
    Local oJson := JsonObject():New()

    Local cCode := "" /*Column B3A_CODIGO*/
    Local cProvReg := "" /*Column B3A_CODOPE*/
    Local cBranch := "" /*Column B3A_FILIAL*/

    Local cSeasonality := "" /*Column B3A_SZNLDD*/
    Local cType := "" /*Column B3A_TIPO*/
    Local cDescription := "" /*Column B3A_DESCRI*/
    Local cActive := "" /*Column B3A_ATIVO*/
    Local nDueDtNotif := 0 /*Column B3A_AVVCTO*/

	oResult:activate()
	oResult:UTSetAPI("/healthcare/v1/obligations"+;
					"?page=1"+;
					"&pageSize=2"+;
                    "&order=obligationCode,providerRegister,systemBranch,seasonality,obligationType,obligationDescription,activeInactive,dueDateNotification"+;
                    "&fields=obligationCode,providerRegister,systemBranch,seasonality,obligationType,obligationDescription,activeInactive,dueDateNotification";
                    ,"REST")
					
	cRet := oResult:UTGetWS(aHeader)
    oResult:AssertFalse(Empty(cRet), "Não houve retorno para a requisição")

	If !Empty(cRet)

        oJson:fromJson(DecodeUTF8(cRet))

        oResult:assertTrue(oJson["items"][1]["obligationCode"] == cCode, "Valor comparado na coluna B3A_CODIGO de alias obligationCode, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["items"][1]["providerRegister"] == cProvReg, "Valor comparado na coluna B3A_CODOPE de alias providerRegister, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["items"][1]["systemBranch"] == cBranch, "Valor comparado na coluna B3A_FILIAL de alias systemBranch, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["items"][1]["seasonality"] == cSeasonality, "Valor comparado na coluna B3A_SZNLDD de alias seasonality, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["items"][1]["obligationType"] == cType, "Valor comparado na coluna B3A_TIPO de alias obligationType, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["items"][1]["obligationDescription"] == cDescription, "Valor comparado na coluna B3A_DESCRI de alias obligationDescription, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["items"][1]["activeInactive"] == cActive, "Valor comparado na coluna B3A_ATIVO de alias activeInactive, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["items"][1]["dueDateNotification"] == nDueDtNotif, "Valor comparado na coluna B3A_AVVCTO de alias dueDateNotification, nao sao iguais. Retorno:" + cRet)  

	EndIf

	oResult:AssertTrue( oResult:lOk, "" )
	oResult:deactivate()

Return oResult

//Test Insert
METHOD insert_003() CLASS CenObriTestCase

	Local oResult := FWTestHelper():New()

    Local cCode := "" /*Column B3A_CODIGO*/
    Local cProvReg := "" /*Column B3A_CODOPE*/
    Local cBranch := "" /*Column B3A_FILIAL*/

    Local cSeasonality := "" /*Column B3A_SZNLDD*/
    Local cType := "" /*Column B3A_TIPO*/
    Local cDescription := "" /*Column B3A_DESCRI*/
    Local cActive := "" /*Column B3A_ATIVO*/
    Local nDueDtNotif := 0 /*Column B3A_AVVCTO*/

    Local aHeader   := {"Content-Type: application/json"}
    Local cRet      := ""
    Local oJson := JsonObject():New()
	Local cBody := '{ ' +;
                        ' "obligationCode": "'+cCode+'",' +;
                        ' "providerRegister": "'+cProvReg+'",' +;
                        ' "systemBranch": "'+cBranch+'",' +;
                        ' "seasonality": "'+cSeasonality+'",' +;
                        ' "obligationType": "'+cType+'",' +;
                        ' "obligationDescription": "'+cDescription+'",' +;
                        ' "activeInactive": "'+cActive+'",' +;
                        ' "dueDateNotification": '+AllTrim(Str(nDueDtNotif))+'' +;
		            '}'
	oResult:activate()
    oResult:UTSetAPI("/healthcare/v1/obligations";
                    ,"REST")
	cRet := oResult:UTPostWS(EncodeUtf8(cBody),aHeader)
    oResult:AssertFalse(Empty(cRet), "Não houve retorno para a requisição. Verifique se o serviço está no ar.")

	If !Empty(cRet)

        oJson:fromJson(DecodeUTF8(cRet))
		
        oResult:assertTrue(oJson["obligationCode"] == cCode, "Valor comparado na coluna B3A_CODIGO de alias obligationCode, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["providerRegister"] == cProvReg, "Valor comparado na coluna B3A_CODOPE de alias providerRegister, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["systemBranch"] == cBranch, "Valor comparado na coluna B3A_FILIAL de alias systemBranch, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["seasonality"] == cSeasonality, "Valor comparado na coluna B3A_SZNLDD de alias seasonality, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["obligationType"] == cType, "Valor comparado na coluna B3A_TIPO de alias obligationType, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["obligationDescription"] == cDescription, "Valor comparado na coluna B3A_DESCRI de alias obligationDescription, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["activeInactive"] == cActive, "Valor comparado na coluna B3A_ATIVO de alias activeInactive, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["dueDateNotification"] == nDueDtNotif, "Valor comparado na coluna B3A_AVVCTO de alias dueDateNotification, nao sao iguais. Retorno:" + cRet)  

	EndIf

	oResult:deactivate()

Return oResult

//Test Update
METHOD update_004() CLASS CenObriTestCase

	Local oResult := FWTestHelper():New()

    Local cCode := "" /*Column B3A_CODIGO*/
    Local cProvReg := "" /*Column B3A_CODOPE*/
    Local cBranch := "" /*Column B3A_FILIAL*/

    Local cSeasonality := "" /*Column B3A_SZNLDD*/
    Local cType := "" /*Column B3A_TIPO*/
    Local cDescription := "" /*Column B3A_DESCRI*/
    Local cActive := "" /*Column B3A_ATIVO*/
    Local nDueDtNotif := 0 /*Column B3A_AVVCTO*/

    Local aHeader   := {"Content-Type: application/json"}
    Local cRet      := ""
    Local oJson := JsonObject():New()
    Local cBody := '{ ' +;
                        ' "obligationCode": "'+cCode+'",' +;
                        ' "providerRegister": "'+cProvReg+'",' +;
                        ' "systemBranch": "'+cBranch+'",' +;
                        ' "seasonality": "'+cSeasonality+'",' +;
                        ' "obligationType": "'+cType+'",' +;
                        ' "obligationDescription": "'+cDescription+'",' +;
                        ' "activeInactive": "'+cActive+'",' +;
                        ' "dueDateNotification": '+AllTrim(Str(nDueDtNotif))+'' +;
		            '}'
	oResult:activate()
	
	oResult:UTSetAPI("/healthcare/v1/obligations/"+cCode+;
					"?page=1"+;
                    "&providerRegister="+escape(cProvReg)+;
                    "&systemBranch="+escape(cBranch)+;
                    "&pageSize=2";
					,"REST")
	
	cRet := oResult:UTPutWS(EncodeUtf8(cBody),aHeader)
    oResult:AssertFalse(Empty(cRet), "Não houve retorno para a requisição. Verifique se o serviço está no ar.")

	If !Empty(cRet)

        oJson:fromJson(DecodeUTF8(cRet))
		
        oResult:assertTrue(oJson["obligationCode"] == cCode, "Valor comparado na coluna B3A_CODIGO de alias obligationCode, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["providerRegister"] == cProvReg, "Valor comparado na coluna B3A_CODOPE de alias providerRegister, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["systemBranch"] == cBranch, "Valor comparado na coluna B3A_FILIAL de alias systemBranch, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["seasonality"] == cSeasonality, "Valor comparado na coluna B3A_SZNLDD de alias seasonality, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["obligationType"] == cType, "Valor comparado na coluna B3A_TIPO de alias obligationType, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["obligationDescription"] == cDescription, "Valor comparado na coluna B3A_DESCRI de alias obligationDescription, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["activeInactive"] == cActive, "Valor comparado na coluna B3A_ATIVO de alias activeInactive, nao sao iguais. Retorno:" + cRet)  
        oResult:assertTrue(oJson["dueDateNotification"] == nDueDtNotif, "Valor comparado na coluna B3A_AVVCTO de alias dueDateNotification, nao sao iguais. Retorno:" + cRet)  

	EndIf

	oResult:deactivate()

Return oResult

//Test Delete
METHOD delete_005() CLASS CenObriTestCase

	Local oResult := FWTestHelper():New()

    Local cCode := "" /*Column B3A_CODIGO*/
    Local cProvReg := "" /*Column B3A_CODOPE*/
    Local cBranch := "" /*Column B3A_FILIAL*/
	
    Local aHeader   := {"Content-Type: application/json"}
    Local cRet      := ""
    Local oJson := JsonObject():New()
    Local cBody     := ""

	oResult:activate()
	
	oResult:UTSetAPI("/healthcare/v1/obligations/"+cCode+;
					"?page=1"+;
                    "&providerRegister="+escape(cProvReg)+;
                    "&systemBranch="+escape(cBranch)+;
                    "&pageSize=2";
					,"REST")
	
	cRet := oResult:UTDeleteWS(EncodeUtf8(cBody),aHeader)

	oResult:AssertFalse(Empty(cRet), "Não houve retorno para a requisição. Verifique se o serviço está no ar.")
    oResult:AssertTrue(cRet=="204 NoContent", "Retorno diferente de '204 NoContent'. Retorno " + cRet)

	oResult:deactivate()

Return oResult

//Test Erro
METHOD error_006() CLASS CenObriTestCase

	Local oResult := FWTestHelper():New()
	Local oCollection := CenCltObri():New()
    Local cMsg := "Erro caso de teste"

    oCollection:setError(cMsg)
	oResult:activate()
	oResult:AssertTrue(oCollection:getError() == cMsg, "Não retornou a mensagem de erro esperada.")
	
	oCollection:destroy()
	oResult:deactivate()

Return oResult