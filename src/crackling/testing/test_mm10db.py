from re import T
from unittest import result
from crackling.mm10db import transToDNA, AT_percentage, polyT, leadingT, mm10db
from crackling.Constants import *
from crackling.Helpers import printer, runner
from crackling import ConfigManager, cracklingClass
import pytest, os

########################
## Testing leadingT ##
########################
def test_leadingT_onFullATSeq():
    result = leadingT('ATATATATATATATATATATAGG')
    expected = False
    assert expected == result

def test_leadingT_onFullASeq():
    result = leadingT('AAAAAAAAAAAAAAAAAAAAAGG')
    expected = False
    assert expected == result

def test_leadingT_onFullTSeq():
    result = leadingT('TTTTTTTTTTTTTTTTTTTTTGG')
    expected = True
    assert expected == result

def test_leadingT_onFullGSeq():
    result = leadingT('GGGGGGGGGGGGGGGGGGGGGGG')
    expected = False
    assert expected == result

def test_leadingT_onFullCSeq():
    result = leadingT('CCCCCCCCCCCCCCCCCCCCCGG')
    expected = False
    assert expected == result

def test_leadingT_onRepeatingATGCSeq():
    result = leadingT('ATGCATGCATGCATGCATGCAGG')
    expected = False
    assert expected == result

def test_leadingT_onRandomSeq():
    result = leadingT('TTTGTGTCATATTCTTCCTATGG')
    expected = True
    assert expected == result

def test_leadingT_onRandomSeq():
    result = leadingT('TTTGTGTCATATTCTTCCTATGG')
    expected = True
    assert expected == result

def test_leadingT_onEmptyString():
    with pytest.raises(ValueError):
        leadingT('')

def test_leadingT_onShortSeq():
    with pytest.raises(ValueError): 
        leadingT('GACTGG')

def test_leadingT_onLongSeq():
    with pytest.raises(ValueError): 
        leadingT('GACTGGTTTGTGTCATATTCTTCCTGTGG')

def test_leadingT_onNumber():
    with pytest.raises(TypeError):
        leadingT(123456789)

def test_leadingT_onArray():
    with pytest.raises(TypeError): 
        leadingT(['T','A','T','G','T','G','T','G','A','T','A','T','A','C','T','T','G','C','T','G','T','G','G'])

def test_leadingT_onDictionary():
    with pytest.raises(TypeError): 
        leadingT({'ATGCATGCATGCATGCATGCAGG':'ATGCATGCATGCATGCATGCAGG'})


###########################
## Testing AT_percentage ##
###########################
def test_AT_percentage_onFullATSeq():
    result = AT_percentage('ATATATATATATATATATAT')
    expected = 100.00
    assert expected == result

def test_AT_percentage_onFullASeq():
    result = AT_percentage('AAAAAAAAAAAAAAAAAAAA')
    expected = 100.00
    assert expected == result

def test_AT_percentage_onFullTSeq():
    result = AT_percentage('TTTTTTTTTTTTTTTTTTTT')
    expected = 100.00
    assert expected == result

def test_AT_percentage_onFullGSeq():
    result = AT_percentage('GGGGGGGGGGGGGGGGGGGG')
    expected = 0.00
    assert expected == result

def test_AT_percentage_onFullCSeq():
    result = AT_percentage('CCCCCCCCCCCCCCCCCCCC')
    expected = 0.00
    assert expected == result

def test_AT_percentage_onRepeatingATGCSeq():
    result = AT_percentage('ATGCATGCATGCATGCATGC')
    expected = 50.0
    assert expected == result

def test_AT_percentage_onRandomSeq():
    result = AT_percentage('TTTGTGTCATATTCTTCCTA')
    expected = 70.0
    assert expected == result

def test_AT_percentage_onEmptyString():
    with pytest.raises(ValueError):
        AT_percentage('')

def test_AT_percentage_onShortSeq():
    with pytest.raises(ValueError): 
        AT_percentage('GACTGG')

def test_AT_percentage_onLongSeq():
    with pytest.raises(ValueError): 
        AT_percentage('GACTGGTTTGTGTCATATTCTTCCTGTGG')

def test_AT_percentage_onNumber():
    with pytest.raises(TypeError):
        AT_percentage(123456789)

def test_AT_percentage_onArray():
    with pytest.raises(TypeError): 
        AT_percentage(['T','A','T','G','T','G','T','G','A','T','A','T','A','C','T','T','G','C','T','G','T','G','G'])

def test_AT_percentage_onDictionary():
    with pytest.raises(TypeError): 
        AT_percentage({'ATGCATGCATGCATGCATGCAGG':'ATGCATGCATGCATGCATGCAGG'})


###################
## Testing polyT ##
###################
def test_polyT_onFullATSeq():
    result = polyT('ATATATATATATATATATATAGG')
    expected = False
    assert expected == result

def test_polyT_onFullASeq():
    result = polyT('AAAAAAAAAAAAAAAAAAAAAGG')
    expected = False
    assert expected == result

def test_polyT_onFullTSeq():
    result = polyT('TTTTTTTTTTTTTTTTTTTTTGG')
    expected = True
    assert expected == result

def test_polyT_onFullGSeq():
    result = polyT('GGGGGGGGGGGGGGGGGGGGGGG')
    expected = False
    assert expected == result

def test_polyT_onFullCSeq():
    result = polyT('CCCCCCCCCCCCCCCCCCCCCGG')
    expected = False
    assert expected == result

def test_polyT_onRepeatingATGCSeq():
    result = polyT('ATGCATGCATGCATGCATGCAGG')
    expected = False
    assert expected == result

def test_polyT_onRandomSeq():
    result = polyT('TTTGTGTCATATTCTTCCTATGG')
    expected = False
    assert expected == result

def test_polyT_onEmptyString():
    with pytest.raises(ValueError):
        polyT('')

def test_polyT_onShortSeq():
    with pytest.raises(ValueError): 
        polyT('GACTGG')

def test_polyT_onLongSeq():
    with pytest.raises(ValueError): 
        polyT('GACTGGTTTGTGTCATATTCTTCCTGTGG')

def test_polyT_onNumber():
    with pytest.raises(TypeError):
        polyT(123456789)

def test_polyT_onArray():
    with pytest.raises(TypeError): 
        polyT(['T','A','T','G','T','G','T','G','A','T','A','T','A','C','T','T','G','C','T','G','T','G','G'])

def test_polyT_onDictionary():
    with pytest.raises(TypeError): 
        polyT({'ATGCATGCATGCATGCATGCAGG':'ATGCATGCATGCATGCATGCAGG'})


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

def test_polyT_onShortSeq():
    with pytest.raises(ValueError): 
        polyT('GACTGG')

def test_polyT_onLongSeq():
    with pytest.raises(ValueError): 
        polyT('GACTGGTTTGTGTCATATTCTTCCTGTGG')

def test_polyT_onNumber():
    with pytest.raises(TypeError):
        polyT(123456789)

def test_polyT_onArray():
    with pytest.raises(TypeError): 
        polyT(['T','A','T','G','T','G','T','G','A','T','A','T','A','C','T','T','G','C','T','G','T','G','G'])

def test_polyT_onDictionary():
    with pytest.raises(TypeError): 
        polyT({'ATGCATGCATGCATGCATGCAGG':'ATGCATGCATGCATGCATGCAGG'})


#####################
## Testing RNAfold ##
#####################
@pytest.fixture
def RNAfold_setup():
    # Setup
    test_input = [
        'GCTCCTCATGCTGGACATTCGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUU\n'
        'GTTCTGGTTCCTAGTATATCGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUU\n'
        'GTATATCTGGAGAGTTAAGAGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUU\n'
    ]
    with open('input.txt', 'w') as input:
        input.writelines(test_input)
    # NOTE: Everything after yeild is considered teardown as per Pytest documentation. (https://docs.pytest.org/en/7.0.x/how-to/fixtures.html#teardown-cleanup-aka-fixture-finalization)
    yield 
    # Teardown
    os.remove('input.txt')
    os.remove('output.txt')


def test_RNAfold_output(RNAfold_setup):
    # Run RNAfold
    runner(f'RNAfold --noPS -j16 -i input.txt > output.txt',
        shell=True,
        check=True
    )
    # Extract results
    with open('output.txt', 'r') as output:
        result = output.readlines()
    # Expected value
    expected = [
        'GCUCCUCAUGCUGGACAUUCGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUU\n',
        '((.......))(((((..(((((((((.((((....))))...)))))))..))...)))))......((((....))))(((((((...)))))))... (-22.40)\n',
        'GUUCUGGUUCCUAGUAUAUCGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUU\n',
        '.(((((((((..((........))..)))))))))....((((((...((((.(......).)))).)))))).......(((((((...)))))))... (-25.20)\n',
        'GUAUAUCUGGAGAGUUAAGAGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUU\n',
        '.......((((.((((....(((((((.((((....))))...)))))))..))))..))))......((((....))))(((((((...)))))))... (-22.50)\n'
    ]
    
    assert expected == result

####################
## Testing mm10db ##
####################
@pytest.fixture
def mm10db_setup():
    # Setup 
    # (Nothing to setup)
    # NOTE: Everything after yeild is considered teardown as per Pytest documentation. (https://docs.pytest.org/en/7.0.x/how-to/fixtures.html#teardown-cleanup-aka-fixture-finalization)
    yield 
    # Teardown
    os.remove('data/output/test-rnafold-input.txt')
    os.remove('data/output/test-rnafold-output.txt')

def test_mm10db(mm10db_setup):
    # Setup Config Manager
    cm = ConfigManager('data/unit-testing/test_config.ini', lambda x : print(f'configMngr says: {x}'))
    # Bypass optimistion filtering
    cm['general']['optimisation'] = 'ultralow'
    # Create result candidate guide dictionary
    cm.isConfigured()
    result = {
        'ACTCCTCATGCTGGACATTCTGG': {
            'passedAvoidLeadingT'       : CODE_UNTESTED,
            'passedATPercent'           : CODE_UNTESTED,
            'AT'                        : CODE_UNTESTED,
            'passedTTTT'                : CODE_UNTESTED,
            'ssL1'                      : CODE_UNTESTED,
            'ssStructure'               : CODE_UNTESTED,
            'ssEnergy'                  : CODE_UNTESTED,
            'passedSecondaryStructure'  : CODE_UNTESTED,
            'acceptedByMm10db'          : CODE_UNTESTED
        },
        'ATTCTGGTTCCTAGTATATCTGG': {
            'passedAvoidLeadingT'       : CODE_UNTESTED,
            'passedATPercent'           : CODE_UNTESTED,
            'AT'                        : CODE_UNTESTED,
            'passedTTTT'                : CODE_UNTESTED,
            'ssL1'                      : CODE_UNTESTED,
            'ssStructure'               : CODE_UNTESTED,
            'ssEnergy'                  : CODE_UNTESTED,
            'passedSecondaryStructure'  : CODE_UNTESTED,
            'acceptedByMm10db'          : CODE_UNTESTED
        },
        'GTATATCTGGAGAGTTAAGATGG': {
            'passedAvoidLeadingT'       : CODE_UNTESTED,
            'passedATPercent'           : CODE_UNTESTED,
            'AT'                        : CODE_UNTESTED,
            'passedTTTT'                : CODE_UNTESTED,
            'ssL1'                      : CODE_UNTESTED,
            'ssStructure'               : CODE_UNTESTED,
            'ssEnergy'                  : CODE_UNTESTED,
            'passedSecondaryStructure'  : CODE_UNTESTED,
            'acceptedByMm10db'          : CODE_UNTESTED
        }
    }

    # Create expected results candidate guide dictionary
    expected = {
        'ACTCCTCATGCTGGACATTCTGG': {
            'passedAvoidLeadingT'       : CODE_ACCEPTED,
            'passedATPercent'           : CODE_ACCEPTED,
            'AT'                        : 50.0,
            'passedTTTT'                : CODE_ACCEPTED,
            'ssL1'                      : 'GCUCCUCAUGCUGGACAUUCGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUU',
            'ssStructure'               : '((.......))(((((..(((((((((.((((....))))...)))))))..))...)))))......((((....))))(((((((...)))))))...',
            'ssEnergy'                  : '-22.40',
            'passedSecondaryStructure'  : CODE_ACCEPTED,
            'acceptedByMm10db'          : CODE_ACCEPTED
        },
        'ATTCTGGTTCCTAGTATATCTGG': {
            'passedAvoidLeadingT'       : CODE_ACCEPTED,
            'passedATPercent'           : CODE_ACCEPTED,
            'AT'                        : 65.0,
            'passedTTTT'                : CODE_ACCEPTED,
            'ssL1'                      : 'GUUCUGGUUCCUAGUAUAUCGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUU',
            'ssStructure'               : '.(((((((((..((........))..)))))))))....((((((...((((.(......).)))).)))))).......(((((((...)))))))...',
            'ssEnergy'                  : '-25.20',
            'passedSecondaryStructure'  : CODE_REJECTED,
            'acceptedByMm10db'          : CODE_REJECTED
        },
        'GTATATCTGGAGAGTTAAGATGG': {
            'passedAvoidLeadingT'       : CODE_ACCEPTED,
            'passedATPercent'           : CODE_ACCEPTED,
            'AT'                        : 65.0,
            'passedTTTT'                : CODE_ACCEPTED,
            'ssL1'                      : 'GUAUAUCUGGAGAGUUAAGAGUUUUAGAGCUAGAAAUAGCAAGUUAAAAUAAGGCUAGUCCGUUAUCAACUUGAAAAAGUGGCACCGAGUCGGUGCUUUU',
            'ssStructure'               : '.......((((.((((....(((((((.((((....))))...)))))))..))))..))))......((((....))))(((((((...)))))))...',
            'ssEnergy'                  : '-22.50',
            'passedSecondaryStructure'  : CODE_ACCEPTED,
            'acceptedByMm10db'          : CODE_ACCEPTED
        }
    }

    # Run mm10db
    mm10db(result, cm)
    assert expected == result