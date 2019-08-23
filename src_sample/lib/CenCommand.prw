#INCLUDE "TOTVS.CH"

/*/{Protheus.doc} CenCommand
    Classe abstrata para execução de comandos
    @type  Class
    @author everton.mateus
    @since 20190320
/*/
Class CenCommand
	
    Data oExecutor
    
    Method New(oExecutor) Constructor
    Method execute()
    
EndClass

Method New(oExecutor) Class CenCommand
    self:oExecutor    := oExecutor
Return self

Method execute() Class CenCommand
Return self:oExecutor:commit()