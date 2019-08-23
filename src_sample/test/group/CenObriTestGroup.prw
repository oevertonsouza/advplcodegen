#include "PROTHEUS.CH"

CLASS CenObriTestGroup FROM FWDefaultTestSuite

	METHOD CenObriTestGroup() CONSTRUCTOR
	
ENDCLASS

METHOD CenObriTestGroup() CLASS CenObriTestGroup
	_Super:FWDefaultTestSuite()
	Self:AddTestCase(CenObriTestCase():CenObriTestCase() )
Return