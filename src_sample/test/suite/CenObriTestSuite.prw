#include "PROTHEUS.CH"

CLASS CenObriTestSuite FROM FWDefaultTestSuite

	DATA aParam
	
	METHOD CenObriTestSuite() CONSTRUCTOR
	METHOD SetUpSuite()
	METHOD TearDownSuite()
	
ENDCLASS

METHOD CenObriTestSuite() CLASS CenObriTestSuite
	_Super:FWDefaultTestSuite()
	Self:AddTestSuite(CenObriTestGroup():CenObriTestGroup() )
Return

METHOD SetUpSuite() CLASS CenObriTestSuite
Local oHelper := FWTestHelper():New()

oHelper:UTOpenFilial("T1","01")
oHelper:Activate()

Return oHelper

METHOD TearDownSuite() CLASS CenObriTestSuite
	Local oHelper := FWTestHelper():New()
	oHelper:UTRestParam()
Return oHelper