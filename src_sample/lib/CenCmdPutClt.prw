#INCLUDE "TOTVS.CH"

/*/{Protheus.doc} CenCmdPutClt

    @type  Class
    @author everton.mateus
    @since 20190320
/*/
Class CenCmdPutClt From CenCommand
	
    Data oExecutor
    
    Method New(oExecutor) Constructor
    Method execute()
    
EndClass

Method New(oExecutor) Class CenCmdPutClt
    self:oExecutor    := oExecutor
Return self

Method execute() Class CenCmdPutClt
Return self:oExecutor:update()