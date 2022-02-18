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