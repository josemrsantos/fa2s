from ..fa2s import *

def test_BioMedCentral_3_items_getData():
    ''' Create an object with max_items=3 and getData. Is data a list ? Does data have more than 1 element ?'''
    api_bio_med_central = APIBioMedCentral(3)
    data = api_bio_med_central.getData()
    assert isinstance(data, list)
    assert len(data)>0

def test_BioMedCentral_0_items_getData():
    ''' Create an object with max_items=3 and getData. Is data = [] ?'''
    api_bio_med_central = APIBioMedCentral(0)
    data = api_bio_med_central.getData()
    assert data == []

