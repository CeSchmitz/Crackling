from crackling.chopchop import chopchop, G20
from crackling.Constants import *
from crackling import ConfigManager
import pytest

#################
## Testing G20 ##
#################
def test_G20_onFullATSeq():
    result = G20('ATATATATATATATATATATAGG')
    expected = False
    assert expected == result

def test_G20_onFullASeq():
    result = G20('AAAAAAAAAAAAAAAAAAAAAGG')
    expected = False
    assert expected == result

def test_G20_onFullTSeq():
    result = G20('TTTTTTTTTTTTTTTTTTTTTGG')
    expected = False
    assert expected == result

def test_G20_onFullGSeq():
    result = G20('GGGGGGGGGGGGGGGGGGGGGGG')
    expected = True
    assert expected == result

def test_G20_onFullCSeq():
    result = G20('CCCCCCCCCCCCCCCCCCCCCGG')
    expected = False
    assert expected == result

def test_G20_onRepeatingATGCSeq():
    result = G20('ATGCATGCATGCATGCATGCAGG')
    expected = False
    assert expected == result

def test_G20_onRandomSeq():
    result = G20('TTTGTGTCATATTCTTCCTGTGG')
    expected = True
    assert expected == result

def test_G20_onEmptySeq():
    with pytest.raises(ValueError): 
        G20('')

def test_G20_onShortSeq():
    with pytest.raises(ValueError): 
        G20('GACTGG')

def test_G20_onLongSeq():
    with pytest.raises(ValueError): 
        G20('GACTGGTTTGTGTCATATTCTTCCTGTGG')

def test_G20_onNumber():
    with pytest.raises(TypeError): 
        G20(123456789)

def test_G20_onArray():
    with pytest.raises(TypeError): 
        G20(['T','A','T','G','T','G','T','G','A','T','A','T','A','C','T','T','G','C','T','G','T','G','G'])

def test_G20_onDictionary():
    with pytest.raises(TypeError): 
        G20({'ATGCATGCATGCATGCATGCAGG':'ATGCATGCATGCATGCATGCAGG'})

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
        'AAAAAAAAAAAAAAAAAAAAAGG': {
            'passedG20' : CODE_UNTESTED
        },
        'TTTTTTTTTTTTTTTTTTTTTGG': {
            'passedG20' : CODE_UNTESTED
        },
        'GGGGGGGGGGGGGGGGGGGGGGG': {
            'passedG20' : CODE_UNTESTED
        },
        'CCCCCCCCCCCCCCCCCCCCCGG': {
            'passedG20' : CODE_UNTESTED
        },
        'TTTGTGTCATATTCTTCCTGTGG': {
            'passedG20' : CODE_UNTESTED
        },
    }

    # Create expected results candidate guide dictionary
    expected = {
        'AAAAAAAAAAAAAAAAAAAAAGG': {
            'passedG20' : CODE_REJECTED
        },
        'TTTTTTTTTTTTTTTTTTTTTGG': {
            'passedG20' : CODE_REJECTED
        },
        'GGGGGGGGGGGGGGGGGGGGGGG': {
            'passedG20' : CODE_ACCEPTED
        },
        'CCCCCCCCCCCCCCCCCCCCCGG': {
            'passedG20' : CODE_REJECTED
        },
        'TTTGTGTCATATTCTTCCTGTGG': {
            'passedG20' : CODE_ACCEPTED
        },
    }

    # Run chopchop
    chopchop(result, cm)
    assert expected == result