from ..fa2s import *

def test_APIEuropePMC_3_items_getData():
    ''' Create an object with max_items=3 and getData. Is data a list ? Does data have more than 1 element ?'''
    api_europe_pmc = APIEuropePMC(3)
    data = api_europe_pmc.getData()
    assert isinstance(data, list)
    assert len(data)>0 and len(data)<=3

def test_PIEuropePMC_0_items_getData():
    ''' Create an object with max_items=3 and getData. Is data = [] ?'''
    api_europe_pmc = APIEuropePMC(0)
    data = api_europe_pmc.getData()
    assert data == []

