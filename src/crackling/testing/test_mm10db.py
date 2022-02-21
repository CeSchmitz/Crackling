from re import T
from crackling.mm10db import transToDNA, AT_percentage, polyT, leadingT, mm10db
from crackling.Constants import *
from crackling import ConfigManager
import pytest

########################
## Testing leadingT ##
########################
def test_leadingT_onFullATSeq():
    result = leadingT('ATATATATATATATATATATA')
    expected = True
    assert expected == result

def test_leadingT_onFullASeq():
    result = leadingT('AAAAAAAAAAAAAAAAAAAAA')
    expected = True
    assert expected == result

def test_leadingT_onFullTSeq():
    result = leadingT('TTTTTTTTTTTTTTTTTTTTT')
    expected = False
    assert expected == result

def test_leadingT_onFullGSeq():
    result = leadingT('GGGGGGGGGGGGGGGGGGGGG')
    expected = True
    assert expected == result

def test_leadingT_onFullCSeq():
    result = leadingT('CCCCCCCCCCCCCCCCCCCCC')
    expected = True
    assert expected == result

def test_leadingT_onRepeatingATGCSeq():
    result = leadingT('ATGCATGCATGCATGCATGCA')
    expected = True
    assert expected == result

def test_leadingT_onRandomSeq():
    result = leadingT('TTTGTGTCATATTCTTCCTAT')
    expected = False
    assert expected == result

def test_leadingT_onRandomSeq():
    result = leadingT('TTTGTGTCATATTCTTCCTAT')
    expected = False
    assert expected == result

def test_leadingT_onEmptyString():
    with pytest.raises(TypeError):
        leadingT('')

def test_leadingT_onNumber():
    with pytest.raises(TypeError):
        leadingT(123456789)


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

def test_AT_percentage_onEmptyString():
    with pytest.raises(TypeError):
        AT_percentage('')

def test_AT_percentage_onNumber():
    with pytest.raises(TypeError):
        AT_percentage(123456789)


###################
## Testing polyT ##
###################
def test_polyT_onFullATSeq():
    result = polyT('ATATATATATATATATATATA')
    expected = False
    assert expected == result

def test_polyT_onFullASeq():
    result = polyT('AAAAAAAAAAAAAAAAAAAAA')
    expected = False
    assert expected == result

def test_polyT_onFullTSeq():
    result = polyT('TTTTTTTTTTTTTTTTTTTTT')
    expected = True
    assert expected == result

def test_polyT_onFullGSeq():
    result = polyT('GGGGGGGGGGGGGGGGGGGGG')
    expected = False
    assert expected == result

def test_polyT_onFullCSeq():
    result = polyT('CCCCCCCCCCCCCCCCCCCCC')
    expected = False
    assert expected == result

def test_polyT_onRepeatingATGCSeq():
    result = polyT('ATGCATGCATGCATGCATGCA')
    expected = False
    assert expected == result

def test_polyT_onRandomSeq():
    result = polyT('TTTGTGTCATATTCTTCCTAT')
    expected = False
    assert expected == result

def test_polyT_onEmptyString():
    with pytest.raises(TypeError):
        polyT('')

def test_polyT_onNumber():
    with pytest.raises(TypeError):
        polyT(123456789)


########################
## Testing transToDNA ##
########################
def test_transToDNA_onFullAUSeq():
    result = transToDNA('AUAUAUAUAUAUAUAUAUAUA')
    expected = 'ATATATATATATATATATATA'
    assert expected == result

def test_transToDNA_onFullASeq():
    result = transToDNA('AAAAAAAAAAAAAAAAAAAAA')
    expected = 'AAAAAAAAAAAAAAAAAAAAA'
    assert expected == result

def test_transToDNA_onFullUSeq():
    result = transToDNA('UUUUUUUUUUUUUUUUUUUUU')
    expected = 'TTTTTTTTTTTTTTTTTTTTT'
    assert expected == result

def test_transToDNA_onFullGSeq():
    result = transToDNA('GGGGGGGGGGGGGGGGGGGGG')
    expected = 'GGGGGGGGGGGGGGGGGGGGG'
    assert expected == result

def test_transToDNA_onFullCSeq():
    result = transToDNA('CCCCCCCCCCCCCCCCCCCCC')
    expected = 'CCCCCCCCCCCCCCCCCCCCC'
    assert expected == result

def test_transToDNA_onRepeatingAUGCSeq():
    result = transToDNA('AUGCAUGCAUGCAUGCAUGCA')
    expected = 'ATGCATGCATGCATGCATGCA'
    assert expected == result

def test_transToDNA_onRandomSeq():
    result = transToDNA('UUUGUGUCAUAUUCUUCCUAU')
    expected = 'TTTGTGTCATATTCTTCCTAT'
    assert expected == result

def test_transToDNA_onEmptyString():
    with pytest.raises(TypeError):
        transToDNA('')

def test_transToDNA_onNumber():
    with pytest.raises(TypeError):
        transToDNA(123456789)


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
            'passedAvoidLeadingT'       : CODE_UNTESTED,
            'passedATPercent'           : CODE_UNTESTED,
            'passedTTTT'                : CODE_UNTESTED,
            'passedATPercent'           : CODE_UNTESTED,
            'ssL1'                      : CODE_UNTESTED,
            'ssStructure'               : CODE_UNTESTED,
            'ssEnergy'                  : CODE_UNTESTED,
            'passedSecondaryStructure'  : CODE_UNTESTED,
            'acceptedByMm10db'          : CODE_UNTESTED
        },
        'TTTTTTTTTTTTTTTTTTTTT': {
            'passedAvoidLeadingT'       : CODE_UNTESTED,
            'passedATPercent'           : CODE_UNTESTED,
            'passedTTTT'                : CODE_UNTESTED,
            'passedATPercent'           : CODE_UNTESTED,
            'ssL1'                      : CODE_UNTESTED,
            'ssStructure'               : CODE_UNTESTED,
            'ssEnergy'                  : CODE_UNTESTED,
            'passedSecondaryStructure'  : CODE_UNTESTED,
            'acceptedByMm10db'          : CODE_UNTESTED
        },
        'GGGGGGGGGGGGGGGGGGGGG': {
            'passedAvoidLeadingT'       : CODE_UNTESTED,
            'passedATPercent'           : CODE_UNTESTED,
            'passedTTTT'                : CODE_UNTESTED,
            'passedATPercent'           : CODE_UNTESTED,
            'ssL1'                      : CODE_UNTESTED,
            'ssStructure'               : CODE_UNTESTED,
            'ssEnergy'                  : CODE_UNTESTED,
            'passedSecondaryStructure'  : CODE_UNTESTED,
            'acceptedByMm10db'          : CODE_UNTESTED
        },
        'CCCCCCCCCCCCCCCCCCCCC': {
            'passedAvoidLeadingT'       : CODE_UNTESTED,
            'passedATPercent'           : CODE_UNTESTED,
            'passedTTTT'                : CODE_UNTESTED,
            'passedATPercent'           : CODE_UNTESTED,
            'ssL1'                      : CODE_UNTESTED,
            'ssStructure'               : CODE_UNTESTED,
            'ssEnergy'                  : CODE_UNTESTED,
            'passedSecondaryStructure'  : CODE_UNTESTED,
            'acceptedByMm10db'          : CODE_UNTESTED
        },
        'TTTGTGTCATATTCTTCCTGT': {
            'passedAvoidLeadingT'       : CODE_UNTESTED,
            'passedATPercent'           : CODE_UNTESTED,
            'passedTTTT'                : CODE_UNTESTED,
            'passedATPercent'           : CODE_UNTESTED,
            'ssL1'                      : CODE_UNTESTED,
            'ssStructure'               : CODE_UNTESTED,
            'ssEnergy'                  : CODE_UNTESTED,
            'passedSecondaryStructure'  : CODE_UNTESTED,
            'acceptedByMm10db'          : CODE_UNTESTED
        },
    }

    # Create expected results candidate guide dictionary
    expected = {
        'AAAAAAAAAAAAAAAAAAAAA': {
            'passedAvoidLeadingT'       : CODE_UNTESTED,
            'passedATPercent'           : CODE_UNTESTED,
            'passedTTTT'                : CODE_UNTESTED,
            'passedATPercent'           : CODE_UNTESTED,
            'ssL1'                      : CODE_UNTESTED,
            'ssStructure'               : CODE_UNTESTED,
            'ssEnergy'                  : CODE_UNTESTED,
            'passedSecondaryStructure'  : CODE_UNTESTED,
            'acceptedByMm10db'          : CODE_UNTESTED
        },
        'TTTTTTTTTTTTTTTTTTTTT': {
            'passedAvoidLeadingT'       : CODE_UNTESTED,
            'passedATPercent'           : CODE_UNTESTED,
            'passedTTTT'                : CODE_UNTESTED,
            'passedATPercent'           : CODE_UNTESTED,
            'ssL1'                      : CODE_UNTESTED,
            'ssStructure'               : CODE_UNTESTED,
            'ssEnergy'                  : CODE_UNTESTED,
            'passedSecondaryStructure'  : CODE_UNTESTED,
            'acceptedByMm10db'          : CODE_UNTESTED
        },
        'GGGGGGGGGGGGGGGGGGGGG': {
            'passedAvoidLeadingT'       : CODE_UNTESTED,
            'passedATPercent'           : CODE_UNTESTED,
            'passedTTTT'                : CODE_UNTESTED,
            'passedATPercent'           : CODE_UNTESTED,
            'ssL1'                      : CODE_UNTESTED,
            'ssStructure'               : CODE_UNTESTED,
            'ssEnergy'                  : CODE_UNTESTED,
            'passedSecondaryStructure'  : CODE_UNTESTED,
            'acceptedByMm10db'          : CODE_UNTESTED
        },
        'CCCCCCCCCCCCCCCCCCCCC': {
            'passedAvoidLeadingT'       : CODE_UNTESTED,
            'passedATPercent'           : CODE_UNTESTED,
            'passedTTTT'                : CODE_UNTESTED,
            'passedATPercent'           : CODE_UNTESTED,
            'ssL1'                      : CODE_UNTESTED,
            'ssStructure'               : CODE_UNTESTED,
            'ssEnergy'                  : CODE_UNTESTED,
            'passedSecondaryStructure'  : CODE_UNTESTED,
            'acceptedByMm10db'          : CODE_UNTESTED
        },
        'TTTGTGTCATATTCTTCCTGT': {
            'passedAvoidLeadingT'       : CODE_UNTESTED,
            'passedATPercent'           : CODE_UNTESTED,
            'passedTTTT'                : CODE_UNTESTED,
            'passedATPercent'           : CODE_UNTESTED,
            'ssL1'                      : CODE_UNTESTED,
            'ssStructure'               : CODE_UNTESTED,
            'ssEnergy'                  : CODE_UNTESTED,
            'passedSecondaryStructure'  : CODE_UNTESTED,
            'acceptedByMm10db'          : CODE_UNTESTED
        },
    }

    # Run mm10db
    mm10db(result, cm)
    assert expected == result