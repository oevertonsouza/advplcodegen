#INCLUDE "TOTVS.CH"

/*/{Protheus.doc} CenCmdObri
    Classe abstrata para execução de comandos
    @type  Class
    @author everton.mateus
    @since 20190320
/*/
Class CenCmdObri
	
    Data oExecutor
    
    Method New(oExecutor) Constructor
    Method execute()
    
EndClass

Method New(oExecutor) Class CenCmdObri
    self:oExecutor := oExecutor
Return self

Method execute() Class CenCmdObri
Return _Super:execute()