#INCLUDE "TOTVS.CH"

/*/{Protheus.doc} CenCmdPostClt

    @type  Class
    @author everton.mateus
    @since 20190320
/*/
Class CenCmdPostClt From CenCommand
	
    Data oExecutor
    
    Method New(oExecutor) Constructor
    Method execute()
    
EndClass

Method New(oExecutor) Class CenCmdPostClt
    self:oExecutor    := oExecutor
Return self

Method execute() Class CenCmdPostClt
Return self:oExecutor:insert()