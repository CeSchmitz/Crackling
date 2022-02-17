from crackling.mm10db import transToDNA, AT_percentage, polyT, leadingT, mm10db
from crackling.Constants import *
from crackling import ConfigManager

########################
## Testing leadingT ##
########################
def test_leadingT_onRandomSeq():
    result = leadingT('TTTGTGTCATATTCTTCCTAT')
    expected = False
    assert expected == result


###########################
## Testing AT_percentage ##
###########################
def test_AT_percentage_onFullATSeq():
    result = AT_percentage('ATATATATATATATATATATA')
    expected = 100.00
    assert expected == result

def test_AT_percentage_onFullASeq():
    result = AT_percentage('AAAAAAAAAAAAAAAAAAAAA')
    expected = 100.00
    assert expected == result

def test_AT_percentage_onFullTSeq():
    result = AT_percentage('TTTTTTTTTTTTTTTTTTTTT')
    expected = 100.00
    assert expected == result

def test_AT_percentage_onFullGSeq():
    result = AT_percentage('GGGGGGGGGGGGGGGGGGGGG')
    expected = 0.00
    assert expected == result

def test_AT_percentage_onFullCSeq():
    result = AT_percentage('CCCCCCCCCCCCCCCCCCCCC')
    expected = 0.00
    assert expected == result

def test_AT_percentage_onRepeatingATGCSeq():
    result = AT_percentage('ATGCATGCATGCATGCATGCA')
    expected = 52.38095238095238
    assert expected == result

def test_AT_percentage_onRandomSeq():
    result = AT_percentage('TTTGTGTCATATTCTTCCTAT')
    expected = 71.42857142857143
    assert expected == result


###################
## Testing polyT ##
###################
def test_polyT_onRandomSeq():
    result = polyT('TTTGTGTCATATTCTTCCTAT')
    expected = False
    assert expected == result


########################
## Testing transToDNA ##
########################
def test_transToDNA_on():
    result = transToDNA('AACCUUGG')
    expected = 'AACCTTGG'
    assert expected == result


#####################
## Testing RNAfold ##
#####################
def test_RNAfold():
    pass

####################
## Testing mm10db ##
####################
def test_mm10db():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'ultralow'
    # Create result candidate guide dictionary
    result = {
        'AAAAAAAAAAAAAAAAAAAAA': {
            'acceptedBySgRnaScorer' : CODE_UNTESTED,
            'sgrnascorer2score'     : CODE_UNTESTED
        },
        'TTTTTTTTTTTTTTTTTTTTT': {
            'acceptedBySgRnaScorer' : CODE_UNTESTED,
            'sgrnascorer2score'     : CODE_UNTESTED
        },
        'GGGGGGGGGGGGGGGGGGGGG': {
            'acceptedBySgRnaScorer' : CODE_UNTESTED,
            'sgrnascorer2score'     : CODE_UNTESTED
        },
        'CCCCCCCCCCCCCCCCCCCCC': {
            'acceptedBySgRnaScorer' : CODE_UNTESTED,
            'sgrnascorer2score'     : CODE_UNTESTED
        },
        'TTTGTGTCATATTCTTCCTGT': {
            'acceptedBySgRnaScorer' : CODE_UNTESTED,
            'sgrnascorer2score'     : CODE_UNTESTED
        },
    }

    # Create expected results candidate guide dictionary
    expected = {
        'AAAAAAAAAAAAAAAAAAAAA': {
            'acceptedBySgRnaScorer' : CODE_ACCEPTED,
            'sgrnascorer2score'     : 0.6509799174117802
        },
        'TTTTTTTTTTTTTTTTTTTTT': {
            'acceptedBySgRnaScorer' : CODE_REJECTED,
            'sgrnascorer2score'     : -7.721831867973529
        },
        'GGGGGGGGGGGGGGGGGGGGG': {
            'acceptedBySgRnaScorer' : CODE_ACCEPTED,
            'sgrnascorer2score'     : 3.5543409089281313
        },
        'CCCCCCCCCCCCCCCCCCCCC': {
            'acceptedBySgRnaScorer' : CODE_ACCEPTED,
            'sgrnascorer2score'     : 1.221131568891114
        },
        'TTTGTGTCATATTCTTCCTGT': {
            'acceptedBySgRnaScorer' : CODE_REJECTED,
            'sgrnascorer2score'     : -0.18335989838239686
        },
    }

    # Run mm10db
    mm10db(result, cm)
    assert expected == result