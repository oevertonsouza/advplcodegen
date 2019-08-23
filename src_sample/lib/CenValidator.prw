#include "TOTVS.CH"

/*/{Protheus.doc} 
    Classe abstrata de um CenValidator
    @type  Class
    @author lima.everton
    @since 20190402
/*/
Class CenValidator
    Data cMsg

    Method New() Constructor
    Method validate()
    Method getErrMsg()

EndClass

Method New() Class CenValidator
    self:cMsg := ""
Return self

Method validate() Class CenValidator
Return .T.

Method getErrMsg() Class CenValidator
Return self:cMsg
