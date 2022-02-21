from crackling.chopchop import chopchop, G20
from crackling.Constants import *
from crackling import ConfigManager
import pytest

#################
## Testing G20 ##
#################
def test_G20_onFullATSeq():
    result = G20('ATATATATATATATATATATA')
    expected = False
    assert expected == result

def test_G20_onFullASeq():
    result = G20('AAAAAAAAAAAAAAAAAAAAA')
    expected = False
    assert expected == result

def test_G20_onFullTSeq():
    result = G20('TTTTTTTTTTTTTTTTTTTTT')
    expected = False
    assert expected == result

def test_G20_onFullGSeq():
    result = G20('GGGGGGGGGGGGGGGGGGGGG')
    expected = True
    assert expected == result

def test_G20_onFullCSeq():
    result = G20('CCCCCCCCCCCCCCCCCCCCC')
    expected = False
    assert expected == result

def test_G20_onRepeatingATGCSeq():
    result = G20('ATGCATGCATGCATGCATGCA')
    expected = False
    assert expected == result

def test_G20_onRandomSeq():
    result = G20('TTTGTGTCATATTCTTCCTGT')
    expected = True
    assert expected == result

def test_G20_onEmptyString():
    result = G20('')
    expected = False
    assert expected == result

def test_G20_onNumber():
    with pytest.raises(TypeError): 
        G20(123456789)


######################
## Testing chopchop ##
######################
def test_chopchop_onTestDataset():
    # Setup Config Manager
    cm = ConfigManager('data/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'ultralow'
    # Create result candidate guide dictionary
    result = {
        'AAAAAAAAAAAAAAAAAAAAA': {
            'passedG20' : CODE_UNTESTED
        },
        'TTTTTTTTTTTTTTTTTTTTT': {
            'passedG20' : CODE_UNTESTED
        },
        'GGGGGGGGGGGGGGGGGGGGG': {
            'passedG20' : CODE_UNTESTED
        },
        'CCCCCCCCCCCCCCCCCCCCC': {
            'passedG20' : CODE_UNTESTED
        },
        'TTTGTGTCATATTCTTCCTGT': {
            'passedG20' : CODE_UNTESTED
        },
    }

    # Create expected results candidate guide dictionary
    expected = {
        'AAAAAAAAAAAAAAAAAAAAA': {
            'passedG20' : CODE_REJECTED
        },
        'TTTTTTTTTTTTTTTTTTTTT': {
            'passedG20' : CODE_REJECTED
        },
        'GGGGGGGGGGGGGGGGGGGGG': {
            'passedG20' : CODE_ACCEPTED
        },
        'CCCCCCCCCCCCCCCCCCCCC': {
            'passedG20' : CODE_REJECTED
        },
        'TTTGTGTCATATTCTTCCTGT': {
            'passedG20' : CODE_ACCEPTED
        },
    }

    # Run chopchop
    chopchop(result, cm)
    assert expected == result