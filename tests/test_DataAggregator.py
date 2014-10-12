from ..fa2s import *

def test_prepare_output_BioMed():
    api_bio_med_central = APIBioMedCentral(3)
    data = DataAggregator([api_bio_med_central], None).prepare_output()
    assert '<div class="api_title">BioMed Central</div>' in data

def test_prepare_output_BioMed_max_0():
    api_bio_med_central = APIBioMedCentral(0)
    data = DataAggregator([api_bio_med_central], None).prepare_output()
    assert '<p class="fa2s_api">\n<div class="api_title">BioMed Central</div>\n</p>\n' in data
